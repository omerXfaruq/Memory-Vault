"""
End-to-end integration tests for Memory Vault application.

These tests verify the complete application workflow including:
- Application startup
- Database initialization
- API endpoints
- Full user workflows
"""
import pytest
import asyncio
import os
from datetime import datetime
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool

from src.listener import app, get_session
from src.db import *
from src.events import Events
from src.response_logic import ResponseLogic


@pytest.fixture(name="test_session")
def test_session_fixture():
    """Create a test database session."""
    engine = create_engine(
        "sqlite:///test_e2e.db",
        echo=False,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    # Cleanup
    import os
    if os.path.exists("test_e2e.db"):
        os.remove("test_e2e.db")


@pytest.fixture(name="test_client")
def test_client_fixture(test_session: Session):
    """Create a test client with database override."""
    def get_session_override():
        return test_session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


class TestE2EApplication:
    """End-to-end application tests."""

    def test_application_startup(self, test_client):
        """Test that the application starts correctly."""
        # Test health endpoint
        response = test_client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"healthy": True}

    def test_database_initialization(self, test_session):
        """Test that database tables are created correctly."""
        # Verify tables exist by querying them
        users = test_session.exec(select(User)).all()
        reminders = test_session.exec(select(Reminder)).all()
        
        # Should be able to query even if empty
        assert isinstance(users, list)
        assert isinstance(reminders, list)

    def test_complete_user_journey(self, test_session, test_client):
        """Test complete user journey from registration to memory management."""
        # 1. Create a user
        user = UserCreate(
            name="E2E Test User",
            telegram_chat_id=999888777,
        )
        created_user = db_create_user(user, session=test_session)
        assert created_user is not None
        assert created_user.active is True
        
        # 2. Add memories
        memory1 = add_memory(created_user, "My first memory", session=test_session)
        memory2 = add_memory(created_user, "My second memory", session=test_session)
        memory3 = add_memory(created_user, "My third memory", session=test_session)
        
        assert memory1 is not None
        assert memory2 is not None
        assert memory3 is not None
        
        # 3. Verify memories are stored
        memories = list_memories(created_user, session=test_session)
        assert len(memories) == 3
        
        # 4. Count memories
        count = count_memories(created_user, session=test_session)
        assert count == 3
        
        # 5. Select random memories
        random_mems = select_random_memories(created_user, count=2, session=test_session)
        assert len(random_mems) == 2
        assert all(m.user_id == created_user.id for m in random_mems)
        
        # 6. Update schedule
        schedule = add_hours_to_the_schedule(created_user, [9, 10, 11], session=test_session)
        assert "9" in schedule
        assert "10" in schedule
        assert "11" in schedule
        
        # 7. Update GMT
        updated = update_gmt(created_user, gmt=3, session=test_session)
        assert updated.gmt == 3
        
        # 8. Toggle settings
        silent = toggle_silent(created_user, session=test_session)
        assert silent is not None
        
        easyadd = toggle_easyadd(created_user, session=test_session)
        assert easyadd is not None
        
        # 9. Delete a memory
        deleted = delete_last_memory(created_user, session=test_session)
        assert deleted == "My third memory"
        
        # 10. Verify deletion
        remaining = list_memories(created_user, session=test_session)
        assert len(remaining) == 2
        
        # 11. User leaves
        left = leave_user(created_user, session=test_session)
        assert left.active is False
        
        # 12. User rejoins
        rejoined = join_user(created_user, session=test_session)
        assert rejoined.active is True

    def test_multiple_users_isolation(self, test_session):
        """Test that multiple users' data is properly isolated."""
        # Create two users
        user1 = db_create_user(
            UserCreate(name="User 1", telegram_chat_id=111111111),
            session=test_session
        )
        user2 = db_create_user(
            UserCreate(name="User 2", telegram_chat_id=222222222),
            session=test_session
        )
        
        # Add memories to each
        add_memory(user1, "User 1 memory", session=test_session)
        add_memory(user1, "User 1 another", session=test_session)
        add_memory(user2, "User 2 memory", session=test_session)
        
        # Verify isolation
        user1_memories = list_memories(user1, session=test_session)
        user2_memories = list_memories(user2, session=test_session)
        
        assert len(user1_memories) == 2
        assert len(user2_memories) == 1
        assert all(m.user_id == user1.id for m in user1_memories)
        assert all(m.user_id == user2.id for m in user2_memories)

    def test_schedule_management_workflow(self, test_session):
        """Test complete schedule management workflow."""
        user = db_create_user(
            UserCreate(name="Schedule Test", telegram_chat_id=333333333),
            session=test_session
        )
        
        # Start with default schedule
        schedule = get_schedule(user, session=test_session)
        assert schedule == "8"
        
        # Add hours
        schedule = add_hours_to_the_schedule(user, [9, 10, 11], session=test_session)
        assert "9" in schedule
        assert "10" in schedule
        assert "11" in schedule
        
        # Remove an hour
        schedule = remove_hour_from_schedule(user, hour=10, session=test_session)
        assert "10" not in schedule
        assert "9" in schedule
        assert "11" in schedule
        
        # Reset schedule
        schedule = reset_schedule(user, session=test_session)
        assert schedule == "8"

    def test_memory_selection_and_tracking(self, test_session):
        """Test memory selection and last_sent tracking."""
        user = db_create_user(
            UserCreate(name="Selection Test", telegram_chat_id=444444444),
            session=test_session
        )
        
        # Add multiple memories
        for i in range(5):
            add_memory(user, f"Memory {i}", session=test_session)
        
        # Select random memories
        selected = select_random_memories(user, count=3, session=test_session)
        assert len(selected) == 3
        
        # Verify last_sent_reminder_id was updated
        test_session.refresh(user)
        assert user.last_sent_reminder_id == selected[-1].id
        
        # Delete last sent memory
        deleted = delete_last_sent_memory(user, session=test_session)
        assert deleted == selected[-1].reminder
        
        # Verify it's gone
        remaining = list_memories(user, session=test_session)
        assert len(remaining) == 4
        assert all(m.reminder != deleted for m in remaining)

    def test_user_status_retrieval(self, test_session):
        """Test retrieving user status information."""
        user = db_create_user(
            UserCreate(name="Status Test", telegram_chat_id=555555555),
            session=test_session
        )
        
        # Update various settings
        update_gmt(user, gmt=5, session=test_session)
        add_hours_to_the_schedule(user, [12, 13], session=test_session)
        toggle_silent(user, session=test_session)
        
        # Retrieve status
        status = get_user_status(user.telegram_chat_id, session=test_session)
        
        assert status is not None
        assert status.gmt == 5
        assert "12" in status.scheduled_hours
        assert "13" in status.scheduled_hours

    def test_package_memory_workflow(self, test_session):
        """Test adding package-type memories."""
        user = db_create_user(
            UserCreate(name="Package Test", telegram_chat_id=666666666),
            session=test_session
        )
        
        # Add a package
        result = add_package(user, package_id=1, session=test_session)
        assert result is True
        
        # Verify it's stored as "package: 1"
        memories = list_memories(user, session=test_session)
        assert len(memories) == 1
        assert memories[0].reminder == "package: 1"

    def test_events_memory_counting(self):
        """Test Events.get_memory_count function."""
        # Test various scenarios
        assert Events.get_memory_count("", 8) == 0  # Empty schedule
        assert Events.get_memory_count("8", 8) == 1  # Single match
        assert Events.get_memory_count("8,9,10", 9) == 1  # One match in list
        assert Events.get_memory_count("8,8,9", 8) == 2  # Multiple matches
        assert Events.get_memory_count("8,9,10", 11) == 0  # No match
        assert Events.get_memory_count("1,2,3,8,9", 8) == 1  # Match in middle

    def test_events_time_calculation(self):
        """Test Events.get_time_until_next_hour function."""
        time_until = Events.get_time_until_next_hour()
        
        # Should return a float between 0 and 3600 seconds
        assert isinstance(time_until, float)
        assert 0 < time_until <= 3600
        
        # Should be reasonable (not negative, not too large)
        assert time_until > 0
        assert time_until <= 3600

    def test_api_health_endpoint(self, test_client):
        """Test API health endpoint."""
        response = test_client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"healthy": True}

    def test_api_webhook_endpoint_structure(self, test_client):
        """Test webhook endpoint accepts proper structure (without real token)."""
        # The endpoint requires a valid token in the path
        # We can test that it returns proper error for invalid token
        response = test_client.post(
            "/webhook/invalid_token",
            json={"update_id": 1}
        )
        # Should return 404 (invalid token) or 422 (validation error)
        assert response.status_code in [404, 422]

    def test_trigger_endpoint_structure(self, test_client):
        """Test trigger endpoint structure."""
        # Without valid token, should return 404
        response = test_client.post("/trigger_send_user_hourly_memories/invalid_token")
        assert response.status_code in [404, 422]

    def test_database_persistence(self, test_session):
        """Test that data persists across operations."""
        user = db_create_user(
            UserCreate(name="Persistence Test", telegram_chat_id=777777777),
            session=test_session
        )
        user_id = user.id
        
        # Add memory
        add_memory(user, "Persistent memory", session=test_session)
        
        # Retrieve user again
        retrieved = get_user_status(user.telegram_chat_id, session=test_session)
        assert retrieved.id == user_id
        
        # Verify memory is still there
        memories = list_memories(retrieved, session=test_session)
        assert len(memories) == 1
        assert memories[0].reminder == "Persistent memory"

    def test_error_handling_nonexistent_user(self, test_session):
        """Test error handling for non-existent users."""
        fake_user = UserCreate(name="Fake", telegram_chat_id=999999999)
        
        # All these should handle None gracefully
        assert get_schedule(fake_user, session=test_session) is None
        assert list_memories(fake_user, session=test_session) is None
        assert leave_user(fake_user, session=test_session) is None
        assert update_gmt(fake_user, gmt=1, session=test_session) is None
        assert toggle_silent(fake_user, session=test_session) is None
        assert toggle_easyadd(fake_user, session=test_session) is None

    def test_edge_cases(self, test_session):
        """Test various edge cases."""
        user = db_create_user(
            UserCreate(name="Edge Cases", telegram_chat_id=888888888),
            session=test_session
        )
        
        # Empty memory list
        assert count_memories(user, session=test_session) == 0
        assert list_memories(user, session=test_session) == []
        assert select_random_memories(user, count=0, session=test_session) == []
        assert delete_last_memory(user, session=test_session) is False
        
        # Select more than available
        add_memory(user, "Only one", session=test_session)
        selected = select_random_memories(user, count=100, session=test_session)
        assert len(selected) == 1
        
        # Empty schedule operations
        schedule = remove_hour_from_schedule(user, hour=99, session=test_session)
        assert schedule is not None  # Should still return current schedule

