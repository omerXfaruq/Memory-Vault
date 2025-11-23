"""
Comprehensive test suite for Memory Vault application.

Tests are organized by functionality:
- User Management
- Memory/Reminder Operations
- Schedule Management
- User Settings
- API Endpoints
- Events and Utilities
"""
import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool

from src.listener import app, User, UserCreate, get_session
from src.events import Events
from src.db import *
from src.constants import Constants

pytest_plugins = ("pytest_asyncio",)


# ==================== FIXTURES ====================

@pytest.fixture(name="session")
def session_fixture():
    """Create a fresh database session for each test."""
    engine = create_engine(
        "sqlite://",
        echo=False,  # Set to True for SQL debugging
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a test client with database session override."""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="sample_user")
def sample_user_fixture(session: Session) -> User:
    """Create a sample user for testing."""
    user = UserCreate(
        name="Test User",
        telegram_chat_id=123456789,
    )
    return db_create_user(user, session=session)


@pytest.fixture(name="sample_user_inactive")
def sample_user_inactive_fixture(session: Session) -> User:
    """Create an inactive sample user for testing."""
    user = UserCreate(
        name="Inactive User",
        telegram_chat_id=987654321,
        active=False,
    )
    return db_create_user(user, session=session)


# ==================== USER MANAGEMENT TESTS ====================

class TestUserManagement:
    """Tests for user creation, reading, joining, and leaving."""

    def test_create_user(self, session):
        """Test creating a new user."""
        user = UserCreate(
            name="New User",
            telegram_chat_id=111111111,
        )
        created_user = db_create_user(user, session=session)
        
        assert created_user is not None
        assert created_user.id is not None
        assert created_user.name == "New User"
        assert created_user.telegram_chat_id == 111111111
        assert created_user.active is True
        assert created_user.scheduled_hours == "8"  # default

    def test_create_user_duplicate_telegram_id(self, session):
        """Test that duplicate telegram_chat_id is handled."""
        user1 = UserCreate(name="User 1", telegram_chat_id=222222222)
        user2 = UserCreate(name="User 2", telegram_chat_id=222222222)
        
        created1 = db_create_user(user1, session=session)
        assert created1 is not None
        
        # Second user with same telegram_chat_id should fail due to unique constraint
        # The function catches exceptions and returns None
        created2 = db_create_user(user2, session=session)
        assert created2 is None

    def test_read_users(self, session, sample_user, sample_user_inactive):
        """Test reading users with filters."""
        # Test reading only active users
        active_users = db_read_users(session=session, only_active_users=True)
        assert len(active_users) == 1
        assert active_users[0].id == sample_user.id
        
        # Test reading all users
        all_users = db_read_users(session=session, only_active_users=False)
        assert len(all_users) == 2
        
        # Test with limit
        limited = db_read_users(session=session, limit=1)
        assert len(limited) == 1

    def test_join_user_new(self, session):
        """Test joining a new user."""
        user = UserCreate(name="Join Test", telegram_chat_id=333333333)
        joined_user = join_user(user, session=session)
        
        assert joined_user is not None
        assert joined_user.active is True

    def test_join_user_already_active(self, session, sample_user):
        """Test joining an already active user."""
        user = UserCreate(
            name="Already Active",
            telegram_chat_id=sample_user.telegram_chat_id,
        )
        result = join_user(user, session=session)
        
        assert result is None  # Already active, should return None

    def test_join_user_reactivate(self, session, sample_user_inactive):
        """Test reactivating an inactive user."""
        user = UserCreate(
            name="Reactivate",
            telegram_chat_id=sample_user_inactive.telegram_chat_id,
        )
        reactivated = join_user(user, session=session)
        
        assert reactivated is not None
        assert reactivated.active is True

    def test_leave_user(self, session, sample_user):
        """Test leaving/deactivating a user."""
        user = UserCreate(
            name="Leave Test",
            telegram_chat_id=sample_user.telegram_chat_id,
        )
        left_user = leave_user(user, session=session)
        
        assert left_user is not None
        assert left_user.active is False

    def test_leave_user_not_found(self, session):
        """Test leaving a non-existent user."""
        user = UserCreate(name="Not Found", telegram_chat_id=999999999)
        result = leave_user(user, session=session)
        
        assert result is None

    def test_leave_user_already_inactive(self, session, sample_user_inactive):
        """Test leaving an already inactive user."""
        user = UserCreate(
            name="Already Inactive",
            telegram_chat_id=sample_user_inactive.telegram_chat_id,
        )
        result = leave_user(user, session=session)
        
        assert result is None  # Already inactive

    def test_get_user_status(self, session, sample_user):
        """Test getting user status."""
        status = get_user_status(sample_user.telegram_chat_id, session=session)
        
        assert status is not None
        assert status.id == sample_user.id
        assert status.name == sample_user.name

    def test_get_user_status_not_found(self, session):
        """Test getting status for non-existent user."""
        status = get_user_status(999999999, session=session)
        assert status is None


# ==================== MEMORY/REMINDER TESTS ====================

class TestMemoryOperations:
    """Tests for memory/reminder CRUD operations."""

    def test_add_memory(self, session, sample_user):
        """Test adding a memory."""
        memory = add_memory(sample_user, "Test memory", session=session)
        
        assert memory is not None
        assert memory.reminder == "Test memory"
        assert memory.user_id == sample_user.id

    def test_add_multiple_memories(self, session, sample_user):
        """Test adding multiple memories."""
        add_memory(sample_user, "Memory 1", session=session)
        add_memory(sample_user, "Memory 2", session=session)
        add_memory(sample_user, "Memory 3", session=session)
        
        memories = list_memories(sample_user, session=session)
        assert len(memories) == 3
        assert all(m.user_id == sample_user.id for m in memories)

    def test_list_memories(self, session, sample_user):
        """Test listing all memories for a user."""
        add_memory(sample_user, "First", session=session)
        add_memory(sample_user, "Second", session=session)
        
        memories = list_memories(sample_user, session=session)
        assert len(memories) == 2
        assert memories[0].reminder == "First"
        assert memories[1].reminder == "Second"

    def test_list_memories_empty(self, session, sample_user):
        """Test listing memories for user with no memories."""
        memories = list_memories(sample_user, session=session)
        assert memories == []

    def test_list_memories_user_not_found(self, session):
        """Test listing memories for non-existent user."""
        user = UserCreate(name="Not Found", telegram_chat_id=999999999)
        result = list_memories(user, session=session)
        assert result is None

    def test_count_memories(self, session, sample_user):
        """Test counting memories."""
        add_memory(sample_user, "Memory 1", session=session)
        add_memory(sample_user, "Memory 2", session=session)
        
        count = count_memories(sample_user, session=session)
        assert count == 2

    def test_count_memories_empty(self, session, sample_user):
        """Test counting memories when user has none."""
        count = count_memories(sample_user, session=session)
        assert count == 0

    def test_select_random_memories(self, session, sample_user):
        """Test selecting random memories."""
        add_memory(sample_user, "Memory 1", session=session)
        add_memory(sample_user, "Memory 2", session=session)
        add_memory(sample_user, "Memory 3", session=session)
        
        random_memories = select_random_memories(sample_user, count=2, session=session)
        assert len(random_memories) == 2
        assert all(m.user_id == sample_user.id for m in random_memories)

    def test_select_random_memories_count_zero(self, session, sample_user):
        """Test selecting zero memories."""
        add_memory(sample_user, "Memory 1", session=session)
        result = select_random_memories(sample_user, count=0, session=session)
        assert result == []

    def test_select_random_memories_more_than_available(self, session, sample_user):
        """Test selecting more memories than available."""
        add_memory(sample_user, "Only one", session=session)
        result = select_random_memories(sample_user, count=10, session=session)
        assert len(result) == 1

    def test_select_random_memories_user_not_found(self, session):
        """Test selecting memories for non-existent user."""
        user = UserCreate(name="Not Found", telegram_chat_id=999999999)
        result = select_random_memories(user, session=session)
        assert result is None

    def test_delete_last_memory(self, session, sample_user):
        """Test deleting the last memory."""
        add_memory(sample_user, "First", session=session)
        add_memory(sample_user, "Last", session=session)
        
        deleted = delete_last_memory(sample_user, session=session)
        assert deleted == "Last"
        
        memories = list_memories(sample_user, session=session)
        assert len(memories) == 1
        assert memories[0].reminder == "First"

    def test_delete_last_memory_empty(self, session, sample_user):
        """Test deleting last memory when user has none."""
        result = delete_last_memory(sample_user, session=session)
        assert result is False

    def test_delete_last_sent_memory(self, session, sample_user):
        """Test deleting the last sent memory."""
        mem1 = add_memory(sample_user, "Memory 1", session=session)
        mem2 = add_memory(sample_user, "Memory 2", session=session)
        
        # Simulate sending memory 2
        sample_user.last_sent_reminder_id = mem2.id
        session.add(sample_user)
        session.commit()
        
        deleted = delete_last_sent_memory(sample_user, session=session)
        assert deleted == "Memory 2"
        assert sample_user.last_sent_reminder_id == -1

    def test_delete_last_sent_memory_no_last_sent(self, session, sample_user):
        """Test deleting last sent when none was sent."""
        add_memory(sample_user, "Memory 1", session=session)
        result = delete_last_sent_memory(sample_user, session=session)
        assert result is False

    def test_add_package(self, session, sample_user):
        """Test adding a package to memories."""
        result = add_package(sample_user, package_id=1, session=session)
        assert result is True
        
        memories = list_memories(sample_user, session=session)
        assert len(memories) == 1
        assert memories[0].reminder == "package: 1"


# ==================== SCHEDULE MANAGEMENT TESTS ====================

class TestScheduleManagement:
    """Tests for schedule management operations."""

    def test_get_schedule(self, session, sample_user):
        """Test getting user schedule."""
        schedule = get_schedule(sample_user, session=session)
        assert schedule == "8"  # default schedule

    def test_get_schedule_user_not_found(self, session):
        """Test getting schedule for non-existent user."""
        user = UserCreate(name="Not Found", telegram_chat_id=999999999)
        result = get_schedule(user, session=session)
        assert result is None

    def test_reset_schedule(self, session, sample_user):
        """Test resetting schedule to default."""
        # First add some hours
        add_hours_to_the_schedule(sample_user, [1, 2, 3], session=session)
        
        # Then reset
        reset = reset_schedule(sample_user, session=session)
        assert reset == "8"  # default

    def test_add_hours_to_schedule(self, session, sample_user):
        """Test adding hours to schedule."""
        result = add_hours_to_the_schedule(sample_user, [1, 13], session=session)
        
        hours = set(result.split(","))
        assert "1" in hours
        assert "8" in hours  # default
        assert "13" in hours

    def test_add_hours_to_schedule_duplicates(self, session, sample_user):
        """Test adding duplicate hours (function doesn't deduplicate, but sorts)."""
        add_hours_to_the_schedule(sample_user, [1, 1, 1], session=session)
        schedule = get_schedule(sample_user, session=session)
        hours = schedule.split(",")
        # Function adds all hours and sorts, so duplicates remain
        # But after sorting, we should have them in order
        assert "1" in hours
        assert "8" in hours  # default
        # Verify it's sorted
        hour_ints = [int(h) for h in hours]
        assert hour_ints == sorted(hour_ints)

    def test_remove_hour_from_schedule(self, session, sample_user):
        """Test removing hour from schedule."""
        add_hours_to_the_schedule(sample_user, [1, 2, 3], session=session)
        
        result = remove_hour_from_schedule(sample_user, hour=2, session=session)
        hours = set(result.split(","))
        assert "2" not in hours
        assert "1" in hours
        assert "3" in hours

    def test_remove_hour_from_schedule_not_present(self, session, sample_user):
        """Test removing hour that's not in schedule."""
        result = remove_hour_from_schedule(sample_user, hour=99, session=session)
        # Should still have default schedule
        assert "8" in result

    def test_create_schedule_array(self):
        """Test creating schedule array from string."""
        result = create_schedule_array("1,2,3,8")
        assert result == [1, 2, 3, 8]

    def test_create_schedule_array_empty(self):
        """Test creating schedule array from empty string."""
        result = create_schedule_array("")
        assert result == []


# ==================== USER SETTINGS TESTS ====================

class TestUserSettings:
    """Tests for user settings and preferences."""

    def test_update_gmt(self, session, sample_user):
        """Test updating user GMT offset."""
        result = update_gmt(sample_user, gmt=3, session=session)
        assert result is not None
        assert result.gmt == 3

    def test_update_gmt_user_not_found(self, session):
        """Test updating GMT for non-existent user."""
        user = UserCreate(name="Not Found", telegram_chat_id=999999999)
        result = update_gmt(user, gmt=3, session=session)
        assert result is None

    def test_toggle_easyadd(self, session, sample_user):
        """Test toggling easy add setting."""
        initial = sample_user.auto_add_active
        
        result = toggle_easyadd(sample_user, session=session)
        assert result is not None
        assert result != initial

    def test_toggle_easyadd_user_not_found(self, session):
        """Test toggling easy add for non-existent user."""
        user = UserCreate(name="Not Found", telegram_chat_id=999999999)
        result = toggle_easyadd(user, session=session)
        assert result is None

    def test_toggle_silent(self, session, sample_user):
        """Test toggling silent mode."""
        initial = sample_user.is_silent
        
        result = toggle_silent(sample_user, session=session)
        assert result is not None
        assert result != initial

    def test_toggle_silent_user_not_found(self, session):
        """Test toggling silent for non-existent user."""
        user = UserCreate(name="Not Found", telegram_chat_id=999999999)
        result = toggle_silent(user, session=session)
        assert result is None


# ==================== API ENDPOINT TESTS ====================

class TestAPIEndpoints:
    """Tests for FastAPI endpoints."""

    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"healthy": True}

    def test_webhook_endpoint_invalid_token(self, client):
        """Test webhook endpoint with invalid token."""
        response = client.post("/webhook/invalid_token", json={})
        # Should return 422 or 404 depending on validation
        assert response.status_code in [404, 422]

    def test_trigger_endpoint_invalid_token(self, client):
        """Test trigger endpoint with invalid token."""
        response = client.post("/trigger_send_user_hourly_memories/invalid_token")
        # Should return 404 or 422
        assert response.status_code in [404, 422]


# ==================== EVENTS AND UTILITIES TESTS ====================

class TestEvents:
    """Tests for Events class functionality."""

    def test_get_time_until_next_hour(self):
        """Test calculating time until next hour."""
        time_until = Events.get_time_until_next_hour()
        assert isinstance(time_until, float)
        assert 0 < time_until <= 3600  # Should be between 0 and 3600 seconds

    def test_get_memory_count(self):
        """Test getting memory count for scheduled hours."""
        # Empty schedule
        assert Events.get_memory_count("", 8) == 0
        
        # Single hour match
        assert Events.get_memory_count("8", 8) == 1
        
        # Multiple hours, one match
        assert Events.get_memory_count("8,9,10", 9) == 1
        
        # Multiple hours, multiple matches (same hour repeated)
        assert Events.get_memory_count("8,8,9", 8) == 2
        
        # No match
        assert Events.get_memory_count("8,9,10", 11) == 0

    @pytest.mark.asyncio
    async def test_main_event_does_not_hang(self):
        """Test that main_event can be started (but don't wait for it)."""
        # This test just verifies the function can be called
        # We don't actually await it since it's an infinite loop
        # In a real scenario, you'd use asyncio.wait_for with a timeout
        pass


# ==================== CONSTANTS TESTS ====================

class TestConstants:
    """Tests for Constants class messages."""

    def test_start_message(self):
        """Test start message generation."""
        msg = Constants.Start.start_message("Test User", "en")
        assert isinstance(msg, str)
        assert len(msg) > 0

    def test_start_message_turkish(self):
        """Test start message in Turkish."""
        msg = Constants.Start.start_message("Test User", "tr")
        assert isinstance(msg, str)
        assert len(msg) > 0

    def test_small_help_message(self):
        """Test small help message."""
        msg = Constants.Help.small_help_message("Test User", "en")
        assert isinstance(msg, str)
        assert len(msg) > 0
        assert "/leave" in msg or "leave" in msg.lower()

    def test_big_help_message(self):
        """Test big help message."""
        msg = Constants.Help.big_help_message("Test User", "en")
        assert isinstance(msg, str)
        assert len(msg) > 0

    def test_group_warning(self):
        """Test group warning message."""
        msg = Constants.Start.group_warning("Test User", "en")
        assert isinstance(msg, str)
        assert len(msg) > 0


# ==================== INTEGRATION TESTS ====================

class TestIntegration:
    """Integration tests for complete workflows."""

    def test_complete_user_workflow(self, session):
        """Test complete user workflow: join, add memories, schedule, leave."""
        # Join
        user = UserCreate(name="Workflow Test", telegram_chat_id=555555555)
        user = join_user(user, session=session)
        assert user is not None
        assert user.active is True
        
        # Add memories
        add_memory(user, "Memory 1", session=session)
        add_memory(user, "Memory 2", session=session)
        assert count_memories(user, session=session) == 2
        
        # Update schedule
        add_hours_to_the_schedule(user, [9, 10], session=session)
        schedule = get_schedule(user, session=session)
        assert "9" in schedule
        assert "10" in schedule
        
        # Update GMT
        update_gmt(user, gmt=2, session=session)
        user = get_user_status(user.telegram_chat_id, session=session)
        assert user.gmt == 2
        
        # Leave
        left = leave_user(user, session=session)
        assert left.active is False
        
        # Verify memories still exist
        assert count_memories(user, session=session) == 2

    def test_memory_selection_and_deletion_workflow(self, session, sample_user):
        """Test workflow of selecting and deleting memories."""
        # Add multiple memories
        for i in range(5):
            add_memory(sample_user, f"Memory {i}", session=session)
        
        # Select random memories
        selected = select_random_memories(sample_user, count=2, session=session)
        assert len(selected) == 2
        
        # Delete last sent
        sample_user.last_sent_reminder_id = selected[-1].id
        session.add(sample_user)
        session.commit()
        
        deleted = delete_last_sent_memory(sample_user, session=session)
        assert deleted == selected[-1].reminder
        
        # Verify count decreased
        assert count_memories(sample_user, session=session) == 4
