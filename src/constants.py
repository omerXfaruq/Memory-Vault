from .db import default_schedule, get_user_status
from .packages import Packages
import os


class Constants:
    smile = "😊"
    hello = "👋🏻"
    sad = "😔"
    sun_glasses = "😎"

    BROADCAST_CHAT_ID = -1001786782026
    FEEDBACK_FORWARD_CHAT_ID = -683998033
    BOT_ID = 5065052385
    DEV_BOT_ID = 5015215848
    if str(os.environ.get("DEV")) == "true":
        BOT_ID = DEV_BOT_ID

    class Common:
        @staticmethod
        def inactive_user(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return f"{name}, sistemime kayıtlı değilsin, you are not in the system, please join by typing; *join* or /join. {Constants.smile}"
            else:
                return f"{name}, you are not in the system, please join by typing; *join* or /join. {Constants.smile}"

        @staticmethod
        def no_memory_found(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return f"{name}, ne yazık ki hatıra kasan boş. Lütfen bu komutla not ekle *add Cümle* {Constants.smile}"
            else:
                return f"{name}, I could not find any note in your Vault. Please add a note with, *add Sentence* {Constants.smile}"

        @staticmethod
        def unknown_command(name: str, language_code: str = "en") -> str:

            if language_code == "tr":
                return (
                    f"Sevgili {name}, ne yazık ki bu komutu bilmiyorum {Constants.sad}"
                    f"\n- /start veya *start* ile başlangıç mesajını görebilirsin"
                    f"\n- /leave veya *leave* ile günlük hatırlatmaları durdurabilirsin"
                    f"\n- /send veya *send* ile rastgele bir not yollarım"
                    f"\n- *send number* ile çok sayıda not yollarım"
                    f"\n- /status veya *status* ile status bilgini yollarım"
                    f"\n- /list veya *list* ile tüm notlarını gönderirim"
                    f"\nTemel komutlarım bunlardı, günlük takvimi ayarlama vb. diğer tüm detaylı komutları görmek için, *help veya /help"
                )
            else:
                return (
                    f"Dear {name}, unfortunately I do not know that command {Constants.sad}"
                    f"\n- /start or *start* to see the start message"
                    f"\n- /leave or *leave* to deactivate daily reminders"
                    f"\n- /send or *send* to get a random note"
                    f"\n- *send number* to get multiple random notes"
                    f"\n- /status or *status* to get your status information"
                    f"\n- /list or *list* to list notes"
                    f"\nThese were my main commands, to see additional commands like editing daily schedule please use, *help* or /help"
                )

    class Start:
        @staticmethod
        def start_message(name: str, language_code: str = "eng") -> str:
            if language_code == "tr":
                return (
                    f"Merhabalar {name} {Constants.hello}"
                    f"\nHatıra Kasası notlarını kaydetmene imkan sağlar ve her gün sana rastgele notlar yollar."
                    f"\n\nHayatımızda karşılaştığımız güzel ve önemli cümleleri bir yere not almak ve sonrasında onları hatırlamak oldukça zor değil mi {Constants.sad}?"
                    f"\nİşte ben bu sorunu oldukça basit ve kullanması kolay bir yöntemle çözüyorum {Constants.sun_glasses}. Zira karışık çözümleri hayatımıza sokmak zor {Constants.sad}."
                    f"\nBu yöntemdeki güzellik şurada, bana verdiğin her notu elbet bir gün sana yollayacağım. Ne zaman yollayacağımı da düşünmene gerek yok."
                    f"\nBu güzel fikri verdiği için sevgili hanımım Seyyide'ye teşekkür ederim."
                    f"\n- Botu anlatan kısa rehbere geçmek için buyur tıkla, /tutorial1"
                )
            else:
                return (
                    f"Hello {name} {Constants.hello}"
                    f"\nKeeping note of beautiful & important stuff that we come across throughout the life, and later remembering them is quite difficult isn't it 😔? Here is the Memory Vault for the rescue! Just take your notes, and I will occasionally remind them to you 😎"
                    f"\nUnfortunately in this era our days&agendas are very busy and it is very hard to follow something consistently. Memory Vault helps us on this front by continuously reminding our notes to us so that you won't ever forget them. You can use it for"
                    f"\n1. Habit Building"
                    f"\n2. Language Learning"
                    f"\n3. Learning the way of Entrepreneurship"
                    f"\n4. Remembering names"
                    f"\n5. Notetaking"
                    f"\n6. Or, Anything Custom, Memory Vault is very flexible and general solution! "
                    f"\n"
                    f"\n❤️ Sincerely thanks to my dear wife Seyyide for the beautiful idea."
                    f"\n"
                    f"\n- To start to a small tutorial please click, /tutorial1"
                )

        @staticmethod
        def group_warning(name: str, language_code: str = "eng") -> str:
            if language_code == "tr":
                return f"\n*Uyarı*: Hatıra Kasasını gruplarda kullanmak için onu ya admin yapmalısın."
            else:
                return f"*Warning*: To use Memory Vault in groups you need to make it an admin."

    class Help:
        @staticmethod
        def small_help_message(name: str, language_code: str = "eng") -> str:
            if language_code == "tr":
                return (
                    f"\n- /leave ile günlük not hatırlatmasını durdurabilirsin"
                    f"\n- /del ile en son yollanan notu silebilirsin"
                    f"\n- /status ile status bilgini alabilirsin"
                    f"\n- /list ile tüm notlarını görebilirsin"
                    f"\n- /schedule ile tüm takvimini güncelleyebilirsin"
                    f"\n- /mode ile kolay ekleme özelliğini kapatıp açabilirsin"
                    f"\n"
                    f"\nTemel komutlarım bunlardı, günlük takvimi ayarlama vb. diğer komutları görmek için, /helpbig."
                )

            else:
                return (
                    f"\n- /leave to deactivate daily note reminders"
                    f"\n- /del to delete the last sent note"
                    f"\n- /status to get your status information"
                    f"\n- /list to list notes"
                    f"\n- /schedule to customize your schedule and frequency"
                    f"\n- /mode to toggle easy note addition"
                    f"\n"
                    f"\nThese were my main commands, to see additional please use, /helpbig."
                )

        @staticmethod
        def big_help_message(name: str, language_code: str = "eng") -> str:
            if language_code == "tr":
                return (
                    f"\nHafıza Kasası sana her gün, takvimindeki saatlerde kasandan rastgele notlar gönderir."
                    f"\n- /join veya *join* ile günlük gönderimi aktifleştirebilirsin"
                    f"\n- /send veya *send* ile rastgele bir not yollarım"
                    f"\n- *send number* ile çok sayıda not yollarım"
                    f"\n"
                    f"\n- *gmt zaman-dilimi* ile zaman dilimi belirleyebilirsin, varsayılan zaman dilimi *GMT0*'dır"
                    f"\nÖrnek:"
                    f"\nGMT+3: *gmt 3*"
                    f"\nGMT-5: *gmt -5*"
                    f"\n"
                    f"\n- /support veya *support* ile beni nasıl destekleyebileceğini öğrenebilirsin"
                    f"\n- *feedback Cümle* ile bot hakkındaki düşüncelerini veya ƒeedback'lerini yollayabilirsin"
                    f"\n"
                    f"\n*Grup Kullanımı*"
                    f"\n- *Birden fazla Hatıra Kasasına* sahip olmak için beni farklı gruplarda kullanabilirsin. Mesela bir kelime öğrenme grubu kurabilirsin."
                    f"\n- Örnek grup: Kuran'ı Kerim'den Dualar(@PrayersFromQuran)"
                )
            else:
                return (
                    f"\nMemory Vault will send you random notes from your memory vault, at the hours in your schedule every day."
                    f"\n- /join or *join* to activate daily note sending"
                    f"\n- /send or *send* to get a random note"
                    f"\n- *send number* to get multiple random notes"
                    f"\n"
                    f"\n- *gmt timezone* to set your timezone,  the default timezone is *GMT0*"
                    f"\nExamples:"
                    f"\nGMT+3: *gmt 3*"
                    f"\nGMT-5: *gmt -5*"
                    f"\n"
                    f"\n- /support or *support* to learn how to support me"
                    f"\n- *feedback Sentence* to send your thoughts and feedbacks about the bot"
                    f"\n"
                    f"\n*Group Usage*"
                    f"\n- *You can have multiple memory vaults* by using different groups, as an example, can create a *language learning group*"
                    f"\n- Example group: @PrayersFromQuran"
                )

    class Join:
        @staticmethod
        def successful_join(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return (
                    f"Hoşgeldin, sefa geldin {name}! Günlük not yollamayı açtın. Takvimindeki saatlere göre sana hatıra kasandan her gün notlar yollayacağım."
                    f"\nTakvimini görmek için, /status, daha fazla bilgi almak için, /help."
                )
            else:
                return (
                    f"Welcome onboard {name}! "
                    f"\nYou activated daily note sending. I will send you random notes from your memory vault according to your schedule."
                    f"\nTo see your schedule, /status, to get more information, /help"
                )

        @staticmethod
        def already_joined(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return f"{name}, hesabın zaten aktif. Hesabının mevcut durumunu görmek için bu komutu kullanabilirsin, /status."
            else:
                return f"{name}, Your account is already active. You can see your status via, /status."

    class Leave:
        @staticmethod
        def successful_leave(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return (
                    f"Allah'a emanet ol {name}. Günlük not yollamamı kapattın, ama merak etme hatıra kasan benimle."
                    f"İstediğin zaman bu komutlarla geri gelebilirsin, *join veya /join."
                )
            else:
                return (
                    f"Good bye {name}, you deactivated daily note sending. It was nice to have you here. "
                    f"Your memory vault remains with me, you can return whenever you wish with command, *join* or /join."
                )

        @staticmethod
        def already_left(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return f"{name}, hesabın zaten atıl durumda."
            else:
                return f"{name}, Your account is already inactive."

    class Mode:
        @staticmethod
        def inactive_auto(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return (
                    f"{name}, kolay not ekleme özelliğini kapattın. Bundan sonra not eklemek için mesajını gönderdikten sonra bu komutu kullanmalısın, /add"
                    f"\nBu özelliği tekrar açmak için, /mode"
                )
            else:
                return (
                    f"{name}, you closed easy note addition feature. From now on, to add your notes, use this command after you send your message, /add"
                    f"\nTo activate this feature again, /mode"
                )

        @staticmethod
        def active_auto(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return (
                    f"{name}, kolay not ekleme özelliğini açtın. Bundan sonra yolladığın notları direk Hafıza Kasana ekleyeceğim."
                    f"\nBu özelliği kapatmak için, /mode"
                )
            else:
                return (
                    f"{name}, you activated easy note addition system. I will add the notes you send automatically to your Memory Vault."
                    f"\nTo deactivate this feature, /mode"
                )

    class Send:
        @staticmethod
        def send_count_out_of_bound(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return f"{name}, lütfen 1<n<50 arasında bir sayı ver, örn: *send 3*."
            else:
                return f"{name}, please give a number which is 1<n<50, ie: *send 3*."

    class List:
        @staticmethod
        def list_messages(name: str, note_count: int, language_code: str = "en") -> str:
            if language_code == "tr":
                return (
                    f"{name} Destur! {note_count} notun birer birer akacak."
                    f"\n\nHatıra kasasının kapılarını açın!"
                    f"\n*id | not*"
                )
            else:
                return (
                    f"Brace yourself {name}, you will receive {note_count} notes one by one."
                    f"\n\nOpen the gates of the memory vault!"
                    f"\n*id | note*"
                )

    class Add:
        @staticmethod
        def no_sentence(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return f"{name} add kelimesinden sonra bir cümle bulamadım. Lütfen bu komutu kullan: *add Cümle*."
            else:
                return f"There is no sentence found after the word *add*. Please use this command: *add Sentence*"

        @staticmethod
        def already_added(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return f"{name} bu not zaten kasada {Constants.smile}"

            else:
                return (
                    f"{name} the note is already in your memory vault {Constants.smile}"
                )

        @staticmethod
        def success(name: str, language_code: str = "en", note: str = "") -> str:
            if language_code == "tr":
                return (
                    f"{name}, not kasana eklendi. Merak etme, onu güvende tutacağım {Constants.smile}"
                    f"\n"
                    f"\n Eğer son eklediğin notu silmek istiyorsan, bu komutu kullan /undo"
                )

            else:
                return (
                    f"{name}, the note is added to your memory vault. No worries, I will keep it safe {Constants.smile}"
                    f"\n"
                    f"\nIf you want to delete the last added note, you can use /undo"
                )

    class Delete:
        @staticmethod
        def no_message(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return f"{name} henüz bir not göndermedim, not göndermemi istiyorsan bu komutu kullan /send"

            else:
                return f"{name}, I haven't sent you a note yet, use this command if you want to get a note, /send"

        @staticmethod
        def success(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return (
                    f"{name}, not kasadan silindi. Unutulan hatıraya elveda {Constants.sad}"
                    f"\nKomutlar hk. bilgi almak için /help"
                    f"\n"
                    f"\n*Silinen Not*:"
                )
            else:
                return (
                    f"{name}, your note is deleted from your memory vault. Good bye to the forgotten memory {Constants.sad}"
                    f"\nTo learn more about commands, /help"
                    f"\n"
                    f"\n*Deleted Note*:"
                )

    class Schedule:
        @staticmethod
        def empty_schedule(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return f"{name}, takvimin boş, takvimine saatleri eklemek için bu komutu kullanabilirsin: *schedule add hour1 hour2 hour3*, örn: *schedule add 8 12 13*"

            else:
                return f"{name}, your schedule is empty, you can add hours to your schedule via, *schedule add hour1 hour2 hour3*, ie: *schedule add 8 12 13*"

        @staticmethod
        def success(name: str, language_code: str = "en", schedule: str = "") -> str:

            if language_code == "tr":

                return (
                    f"{name}, güncel takvimin aşağıda, takvimine göre rastgele not alacaksın."
                    f"\n"
                    f"\n*Saat - Not Sayısı*: "
                    f"\n{schedule}"
                    f""
                    f"\n\nUyarı: Eğer bu bottan faydalanmak istiyorsan, takvimini dolup taşırmamaya dikkat et ve gelen mesajlara dikkatini ver, göz atıp geçme."
                )
            else:
                return (
                    f"{name}, your current schedule is below, You will get random notes according to your schedule"
                    f"\n"
                    f"\n*Hour - Note Count*: "
                    f"\n{schedule}"
                    f""
                    f"\n\nWarning: If you want to make use of this bot, be careful to not overflow your schedule and give attention to the incoming messages, do not just look and pass."
                )

        @staticmethod
        def no_number_found(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return f"{name}, *schedule add* komutu sonrasında bir sayı bulamadım, doğru kullanım örneği: *schedule add 1 3 5 21*"

            else:
                return f"{name}, there is no numbers found after *schedule add*, correct usage example: *schedule add 1 3 5 21*"

        @staticmethod
        def add_incorrect_number_input(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return f"{name}, lütfen girdi olarak sayılar kullan, 0<=sayı<=23, örn: *schedule add 1 3 5 21*"

            else:
                return f"{name}, please use numbers 0<=number<=23, ie: *schedule add 1 3 5 21*"

        @staticmethod
        def remove_incorrect_number_input(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return f"{name}, lütfen girdi olarak sayı kullan, 0<=sayı<=23, örn: *schedule remove 8*"

            else:
                return (
                    f"{name}, please use number 0<=number<=23, ie: *schedule remove 8*"
                )

        @staticmethod
        def unknown_command(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return (
                    f"Takvimini güncellemek için bu komutları kullanabilirsin."
                    f"\n- /status ile takvimini görebilirsin"
                    f"\n"
                    f"\n- *schedule add 8 12 12 20* ile takvimine saatler ekleyebilir"
                    f"\n- *schedule reset* ile takvimini sıfırlayabilir"
                    f"\n- *schedule remove 8* ile takviminden saat çıkarabilirsin."
                )
            else:
                return (
                    f"To configure your schedule you can use these commands:"
                    f"\n"
                    f"\n- /status to see your current schedule"
                    f"\n"
                    f"\n- *schedule add 8 12 12 20*"
                    f"\n- *schedule reset*"
                    f"\n- *schedule remove 8*"
                )

    class Gmt:
        @staticmethod
        def success(name: str, language_code: str = "en", gmt: int = 0) -> str:
            if language_code == "tr":
                return f"{name}, güncel saat dilimin: GMT{gmt}."
            else:
                return f"{name}, your current timezone is: GMT{gmt}."

        @staticmethod
        def incorrect_timezone(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return f"{name}, lütfen saat dilimini doğru kullan, örn: *gmt 3* or *gmt -3*"
            else:
                return f"{name}, please give your timezone correctly, ie: *gmt 3* or *gmt -3*"

    class Broadcast:
        @staticmethod
        def no_sentence_found(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return f"{name}, *broadcast* kelimesi sonrasında herhangi bir cümle bulamadım {Constants.sad}, doğru örn: *broadcast Cümle*"
            else:
                return f"{name}, there is no sentence found after the word *broadcast* {Constants.sad}, correct usage: *broadcast Sentence*"

        @staticmethod
        def success(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return f"{name}, broadcast yollandı {Constants.smile}"
            else:
                return f"{name}, broadcast is sent {Constants.smile}"

        @staticmethod
        def no_right(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return f"{name}, broadcast hakkın yok {Constants.smile}"
            else:
                return f"{name}, you have no broadcast right {Constants.smile}"

    class Status:
        @staticmethod
        def get_status(
            name: str,
            language_code: str = "en",
            gmt: int = 0,
            active: bool = True,
            schedule: str = "",
            auto_add: bool = True,
            note_count: int = 0,
        ) -> str:
            if language_code == "tr":
                daily_is_active = "aktif" if active else "pasif"
                auto_add_is_active = "aktif" if auto_add else "pasif"

                return (
                    f"Mevcut durumun:"
                    f"\n- Gmt: *GMT{gmt}*"
                    f"\n- Günlük gönderim: *{daily_is_active}*"
                    f"\n- Kolay not ekleme: *{auto_add_is_active}*"
                    f"\n- Hatıra Kasandaki not sayısı: {note_count}"
                    f"\n- Takvim: (saat - not adeti)"
                    f"\n{schedule}"
                    f"\n"
                    f"\nUyarı: Eğer bu bottan faydalanmak istiyorsan, takvimini dolup taşırmamaya dikkat et ve gelen mesajlara dikkatini ver, göz atıp geçme."
                )
            else:
                daily_is_active = "active" if active else "passive"
                auto_add_is_active = "active" if auto_add else "passive"

                return (
                    f"Your current status:"
                    f"\n- Gmt: *GMT{gmt}*"
                    f"\n- Daily sending: *{daily_is_active}*"
                    f"\n- Easy add: *{auto_add_is_active}*"
                    f"\n- Number of notes in the Vault: {note_count}"
                    f"\n- Schedule: (hour - note count)"
                    f"\n{schedule}"
                    f"\n"
                    f"\nWarning: If you want to make use of this bot, be careful to not overflow your schedule and give attention to the incoming messages, do not just look and pass."
                )

    class Feedback:
        @staticmethod
        def no_message(name: str, language_code: str = "en"):
            if language_code == "tr":
                return f"{name}, *feedback* sonrasında bir cümle bulamadım {Constants.sad}, doğru örnek: *feedback Cümle*"
            else:
                return f"{name}, there is no message found after the word *feedback* {Constants.sad}, correct example: *feedback Sentence*"

        @staticmethod
        def success(name: str, language_code: str = "en", feedback: str = ""):
            if language_code == "tr":
                return (
                    f"{name}, feedback'ini yöneticiye ilettim, desteğin için çok teşekkür ederim {Constants.smile}"
                    f"\nFeedback: *{feedback}*"
                )
            else:
                return (
                    f"{name}, I forwarded your feedback to the admin, thank you for your support {Constants.smile}"
                    f"\nFeedback: *{feedback}*"
                )

        @staticmethod
        def fail(name: str, language_code: str = "en"):
            if language_code == "tr":
                return f"{name}, feedback'i yöneticiye iletemedim, bir hata oluştu."
            else:
                return f"{name}, I could not forward your feedback to the admin, an error occurred."

    class Support:
        @staticmethod
        def support(name: str, language_code: str = "en"):
            if language_code == "tr":
                return (
                    f"Teşekkür ederim {name}, beni desteklemek için"
                    f"\n- @memory_vault_bot'u arkadaşlarınla paylaşabilir"
                    f"\n- Bu komutla bana feedback verebilirsin, *feedback cümle*"
                    f"\n- Github repo'ma yıldız verebilirsin, https://github.com/FarukOzderim/Memory-Vault/"
                )
            else:
                return (
                    f"Thank you {name}, to support me you can"
                    f"\n- Share me with your friends"
                    f"\n- Give feedback using the command, *feedback sentence*"
                    f"\n- Star the github repository at https://github.com/FarukOzderim/Memory-Vault/"
                )

    class Tutorial:
        @staticmethod
        def tutorial_1(name: str, language_code: str = "en"):
            if language_code == "tr":
                return (
                    f"*gmt zaman-dilimi* ile zaman dilimi belirleyebilirsin, varsayılan zaman dilimi *GMT0*'dır, Türkiye ise GMT+3 zaman diliminde."
                    f"\nÖrnek:"
                    f"\nGMT+3: *gmt 3*"
                    f"\nGMT0: *gmt 0*"
                    f"\nGMT-5: *gmt -5*"
                    f"\n\nBir sonraki rehber adımına geçmek için, /tutorial2"
                )
            else:
                return (
                    f"Use *gmt timezone* to set your timezone, the default timezone is *GMT0*. Btw New York is GMT-5, London is GMT0, Malaysia is GMT+8."
                    f"\nExamples:"
                    f"\nGMT+3: *gmt 3*"
                    f"\nGMT0: *gmt 0*"
                    f"\nGMT-5: *gmt -5*"
                    f"\n\nFor the next tutorial step please use, /tutorial2"
                )

        @staticmethod
        def tutorial_2(name: str, language_code: str = "en"):
            if language_code == "tr":
                return (
                    f"Kasana not eklemek herhangi bir mesaj yolla, yazı, media veya iletme yollayabilirsin. İleride sana her gün rastgele bir not hatırlatacağım."
                    f"\n\nBir sonraki rehber adımına geçmek için, /tutorial3"
                )
            else:
                return (
                    f"To add a note to your Vault, just send any message, text, media, forward, etc. Later, I will remind you a random note everyday."
                    f"\n\nFor the next tutorial step please use, /tutorial3"
                )

        @staticmethod
        def tutorial_3(name: str, language_code: str = "en"):
            if language_code == "tr":
                return (f"Constants.Help.small_help_message(name, language_code)"
                        f"\n"
                        f"\nTebrikler {name}! Rehberi tamamladın, seninle çıkacağamız yolculuk için çok heyecanlıyım 🤗"
                        )
            else:
                return (f"Constants.Help.small_help_message(name, language_code)"
                        f"\n"
                        f"\nCongratulatıons {name}! You completed the tutorials, let's have great journey together 🤗"
                        )

    class Package:
        @staticmethod
        def help(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return (
                    f"Hatıra kasasına hazır paketler de ekleyebilirsin.\n"
                    f"Paket eklemek için, package add package-no, kullanabilirsin\n"
                    f"örn: *package add 0*"
                )
            else:
                return (
                    f"You can also add preprepared packages to your Memory Vault.\n"
                    f"To add a package you can use, package add package-no\n"
                    f"ex: *package add 0*"
                )

        @staticmethod
        def incorrect_id(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return f"{name}, verdiğin paket numarası yanlış. Lütfen doğru bir paket numarası ver, 0 <= x <= {len(Packages.functions) - 1} \nörnek: *package add 0*"

            else:
                return f"{name}, the package id is incorrect. Please provide a correct id, 0 <= x <= {len(Packages.functions) - 1} \nex: *package add 0*"

        @staticmethod
        def success(name: str, language_code: str = "en", package_id: int = 0) -> str:
            if language_code == "tr":
                return (
                    f"{name}, {Packages.titles[package_id]} başarıyla kasana eklendi."
                )
            else:
                return f"{name}, {Packages.titles[package_id]} is successfully added to your vault."

        @staticmethod
        def already_added(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return f"{name}, verdiğin paket numarası zaten ekli durumda."

            else:
                return f"{name}, the package id you gave is already added to the Vault."

        @staticmethod
        def unknown_command(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return (
                    f"{name}, bu komutu bilmiyorum.\n\n"
                    f"{Constants.Package.help(name, language_code)}"
                )
            else:
                return (
                    f"{name}, I do not know that command.\n\n"
                    f"{Constants.Package.help(name, language_code)}"
                )
