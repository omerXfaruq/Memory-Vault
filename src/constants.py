from .db import default_schedule, get_user_status


class Constants:
    smile = "😊"
    hello = "👋🏻"
    sad = "😔"
    sun_glasses = "😎"

    BROADCAST_CHAT_ID = -1001786782026
    FEEDBACK_FORWARD_CHAT_ID = -683998033
    BOT_ID = 5065052385

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
                return f"{name}, ne yazık ki hatıra kasan boş. Lütfen bu komutla hatıra ekle *add Cümle* {Constants.smile}"
            else:
                return f"{name}, I could not find any memory in your Vault. Please add a memory with, *add Sentence* {Constants.smile}"

        @staticmethod
        def unknown_command(name: str, language_code: str = "en") -> str:
            help_message = Constants.Help.help_message(name, language_code)

            if language_code == "tr":
                return (
                    f"Sevgili {name}, ne yazık ki bu komutu bilmiyorum {Constants.sad}, sana yardım mesajımı yollayayım, /help."
                    f"\n{help_message}"
                )
            else:
                return (
                    f"Dear {name}, unfortunately I do not know that command {Constants.sad}, let me send you my /help message."
                    f"\n{help_message}"
                )

    class Start:
        @staticmethod
        def start_message(name: str, language_code: str = "eng") -> str:
            if language_code == "tr":
                return (
                    f"Merhabalar {name} {Constants.hello}"
                    f"\nHatıra Kasası notlarını(hatıralarını) kaydetmene imkan sağlar ve sana her gün Kasandan rastgele hatıralar yollar."
                    f"\n\nHayatımızda karşılaştığımız güzel ve önemli cümleleri bir yere not almak ve sonrasında onları hatırlamak oldukça zor değil mi? {Constants.sad}"
                    f"\nİşte ben bu sorunu oldukça basit ve kullanması kolay bir yöntemle çözüyorum {Constants.sun_glasses}. Zira karışık çözümleri hayatımıza sokmak zor {Constants.sad}."
                    f"\nBu yöntemdeki güzellik şurada, bana verdiğin her hatırayı elbet bir gün sana yollayacağım. Ne zaman yollayacağımı da düşünmene gerek yok."
                    f"\nBu güzel fikri verdiği için sevgili hanımım Seyyide'ye teşekkür ederim."
                    f"\n\n- Botu kullanmaya başlamak için buyur tıkla, /join"
                    f"\n- Botu anlatan kısa rehbere geçmek için buyur tıkla, /tutorial1"
                )
            else:
                return (
                    f"Hello {name} {Constants.hello}"
                    f"\nMemory Vault stores your notes(memories) in the memory vault and sends you random memories every day."
                    f"\n\nKeeping note of beautiful & important stuff that we come across throughout the life, and later remembering them is quite difficult isn't it? {Constants.sad}"
                    f"\nHere is the Memory Vault for the rescue! I solve this problem with a very simple and easy to use method {Constants.sun_glasses}. Because, complex methods makes it harder to keep them in our life."
                    f"\nHere is the catch, I will definitely send you each memory you give to me one day. And you don't need to think over when I will send it."
                    f"\nSincerely thanks to my dear wife Seyyide for the beautiful idea."
                    f"\n\n- To start using the bot please click, /join"
                    f"\n- To start to a small tutorial please click, /tutorial1"
                )

    class Help:
        @staticmethod
        def help_message(name: str, language_code: str = "eng") -> str:
            if language_code == "tr":
                return (
                    f"\n\nHafıza Kasası sana her gün, takvimini izleyerek kasandan rastgele hatıralar gönderir."
                    f"\n- /help veya *help* yardım mesajını alabilirsin"
                    f"\n- /join veya *join* ile günlük gönderimi aktifleştirebilirsin"
                    f"\n- /leave veya *leave* ile günlük yollamayı durdurabilirsin"
                    f"\n- /send veya *send* ile rastgele bir hatıra yollarım"
                    f"\n- *send number* ile çok sayıda hatıra yollarım"
                    f"\n- /status veya *status* ile status bilgini yollarım"
                    f"\n- /list veya *list* ile tüm hatıralarını gönderirim"
                    f"\n\n- *add Memory* ile kasana bir hatıra ekleyebilirsin"
                    f"\nÖrnek:"
                    f"\n*add Vakit hiç bir zaman geri gelmez*"
                    f"\n\n- *delete id* ile bir hatırayı silebilirsin. Hatıra id'lerini bu komutlarla öğrenebilirsin, *list* veya /list"
                    f"\nÖrnek:"
                    f"\n*delete 2*"
                    f"\n\n- *gmt zaman-dilimi* ile zaman dilimi belirleyebilirsin, varsayılan zaman dilimi *GMT0*'dır"
                    f"\nÖrnek:"
                    f"\nGMT+3: *gmt 3*"
                    f"\nGMT0: *gmt 0*"
                    f"\nGMT-5: *gmt -5*"
                    f"\n\n- /support veya *support* ile beni nasıl destekleyebileceğini öğrenebilirsin"
                    f"\n- *feedback Cümle* ile bot hakkındaki düşüncelerini veya ƒeedback'lerini yollayabilirsin"
                    f"\n\n*Schedule(takvim) hakkındaki komutlar:*"
                    f"\nHer gün takvimindeki saat başlarında sana hatıralar yollarım. Varsayılan takvim saatleri *{default_schedule}*'dır. Yani her gün 8:00 ve 20:00'de sana bir adet hatıra yollayacağım."
                    f"\nSchedule komutlarıyla kendi günlük takvimini oluşturabilirsin. Ayrıca bir saati birden fazla kez ekleyerek o saatte birden çok hatıra alabilirsin."
                    f"\n- /schedule veya *schedule* ile şuanki takvimini yollarım"
                    f"\n- *schedule reset* ile takvimini varsayılan takvime({default_schedule}) çekerim"
                    f"\n- *schedule add saat1 saat2 saat3* ile saatleri takvimine eklerim"
                    f"\nÖrnek:"
                    f"\n*schedule add 1 3 9 11*"
                    f"\n- *schedule remove saat* ile bir saati takviminden tamamen kaldırabilirsin"
                    f"\nÖrnek:"
                    f"\n*schedule remove 8*"
                    f"\n\n- Beni *gruplarda da kullanabilirsin*, gruba ekleyip yönetici yapman yeterli. Yönetici yapmak istemiyorsan da grupta benim mesajlarıma yanıtla yaparak da komutları kullanabilirsin."
                    f"\n- *Birden fazla Hatıra Kasasına* sahip olmak için beni farklı gruplarda kullanabilirsin. Örneğin hatırlamak istediğin kelimeleri hatıralar olarak eklediğin bir dil öğrenme grubunda sana güzelce hizmet ederim."
                    f"\n- Örnek grup: Kuran'ı Kerim'den Dualar(@PrayersFromQuran)"
                )
            else:
                return (
                    f"\n\nMemory Vault will send you random memories from your memory vault every day."
                    f"\n- /help or *help* to get help message"
                    f"\n- /join or *join* to activate daily memory sending"
                    f"\n- /leave or *leave* to deactivate daily sending"
                    f"\n- /send or *send* to get a random memory"
                    f"\n- *send number* to get multiple random memories"
                    f"\n- /status or *status* to get your status information"
                    f"\n- /list or *list* to list memories"
                    f"\n\n- *add Memory* to add a memory to your memory vault"
                    f"\nExample:"
                    f"\n*add Time never does come back*"
                    f"\n\n- *delete id* to delete a memory. You can learn the memory ids with the command, *list* or /list"
                    f"\nExample:"
                    f"\n*delete 2*"
                    f"\n\n- *gmt timezone* to set your timezone,  the default timezone is *GMT0*"
                    f"\nExamples:"
                    f"\nGMT+3: *gmt 3*"
                    f"\nGMT0: *gmt 0*"
                    f"\nGMT-5: *gmt -5*"
                    f"\n\n- /support or *support* to learn how to support me"
                    f"\n- *feedback Sentence* to send your thoughts and feedbacks about the bot"
                    f"\n\n*Schedule related commands:*"
                    f"\nI send memories according to the hours in your schedule. Default schedule hours are *{default_schedule}*. I will send you a memory at 8:00 and 20:00 everyday."
                    f"\nYou can create your own daily schedule. Furthermore you can add an hour multiple times to receive multiple memories at that hour."
                    f"\n- /schedule or *schedule* to display your current schedule"
                    f"\n- *schedule reset* to reset your schedule to the default schedule"
                    f"\n- *schedule add hour1 hour2 hour3* to add hours to your schedule"
                    f"\nExample:"
                    f"\n*schedule add 1 3 9 11*"
                    f"\n- *schedule remove hour* to remove an hour from your schedule"
                    f"\nExample:"
                    f"\n*schedule remove 8*"
                    f"\n\n- You can *use me in groups* as well, just add me to a group and promote me to admin there. If you don't want to make me an admin, you can reply to my messages in the group to use my commands."
                    f"\n- Furthermore *you can have multiple memory vaults* by using different groups. For example I would serve you well in a *language learning group*, where you add words you want to remember to your memory vault."
                    f"\n- Example group: @PrayersFromQuran"
                )

    class Join:
        @staticmethod
        def successful_join(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return (
                    f"Hoşgeldin, sefa geldin {name}! Günlük hatıra yollamayı açtın. Takvimindeki saatlere göre sana hatıra kasandan her gün hatıralar yollayacağım."
                    f"Varsayılan takvimindeki saatleri {default_schedule}'dır. (8 -> 8:00, 20 -> 20:00). Daha detaylı bilgi için, *help* veya /help."
                    f"\nYeni bir kullanıcı isen lütfen bu komuta tıklayarak rehbere başla, /tutorial1 {Constants.smile}"
                )
            else:
                return (
                    f"Welcome onboard {name}! "
                    f"\nYou activated daily memory sending. I will send you random memories from your memory vault according to your schedule."
                    f"The default hours in the schedule are {default_schedule}(8 -> 8:00, 20 -> 20:00). You can get more detailed information by writing, *help* or /help."
                    f"\nIf you are a new user, please start the tutorial by clicking, /tutorial1 {Constants.smile}"
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
                    f"Allah'a emanet ol {name}. Günlük hatıra yollamamı kapattın, ama merak etme hatıra kasan benimle."
                    f"İstediğin zaman bu komutlarla geri gelebilirsin, *join veya /join."
                )
            else:
                return (
                    f"Good bye {name}, you deactivated daily memory sending. It was nice to have you here. "
                    f"Your memory vault remains with me, you can return whenever you wish with command, *join* or /join."
                )

        @staticmethod
        def already_left(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return f"{name}, hesabın zaten atıl durumda."
            else:
                return f"{name}, Your account is already inactive."

    class Send:
        @staticmethod
        def send_count_out_of_bound(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return f"{name}, lütfen 1<n<50 arasında bir sayı ver, örn: *send 3*."
            else:
                return f"{name}, please give a number which is 1<n<50, ie: *send 3*."

    class List:
        @staticmethod
        def list_messages(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return (
                    f"{name} Destur! Hatıraların birer birer akacak."
                    f"\n\nHatıra kasasının kapılarını açın!"
                    f"\n*id | hatıra*"
                )
            else:
                return (
                    f"Brace yourself {name}, you will receive memories one by one."
                    f"\n\nOpen the gates of the memory vault!"
                    f"\n*id | memory*"
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
                return f"{name} bu hatıra zaten kasada {Constants.smile}"

            else:
                return f"{name} the memory is already in your memory vault {Constants.smile}"

        @staticmethod
        def success(name: str, language_code: str = "en", memory: str = "") -> str:
            if language_code == "tr":
                return (
                    f"{name}, hatıran kasana eklendi. Merak etme, onu güvende tutacağım {Constants.smile}"
                    f"\n*Hatıra*: \n{memory}"
                )

            else:
                return (
                    f"{name}, memory is added to your memory vault. No worries, I will keep it safe {Constants.smile}"
                    f"\n*Memory*: \n{memory}"
                )

    class Delete:
        @staticmethod
        def no_id(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return f"{name}, bana hatıranın id'sini vermen gerekiyor, örn: *delete 2*, bu komut ile id'leri öğrenebilirsin *list* veya /list"

            else:
                return f"{name}, need to give me id of the memory, ie: *delete 2*, you can get it by using command, *list* or /list"

        @staticmethod
        def success(name: str, language_code: str = "en", memory: str = "") -> str:
            if language_code == "tr":
                return (
                    f"{name}, hatıran kasadan silindi. Unutulan hatıraya elveda {Constants.sad}"
                    f"\n*Silinen Hatıra*:"
                    f"\n{memory}"
                )
            else:
                return (
                    f"{name}, your memory is deleted from your memory vault. Good bye to the forgotten memory {Constants.sad}"
                    f"\n*Deleted Memory*:"
                    f"\n{memory}"
                )

    class Schedule:
        @staticmethod
        def empty_schedule(name: str, language_code: str = "en") -> str:
            if language_code == "tr":
                return f"{name}, takvimin boş, takvimine saatleri eklemek için bu komutu kullanabilirsin: *schedule add hour1 hour2 hour3*, örn: *schedule add 8 12*"

            else:
                return f"{name}, your schedule is empty, you can add hours to your schedule via, *schedule add hour1 hour2 hour3*, ie: *schedule add 8 12*"

        @staticmethod
        def success(name: str, language_code: str = "en", schedule: str = "") -> str:
            if language_code == "tr":
                return (
                    f"{name}, güncel takvimin aşağıda, takvimindeki saat başlarında rastgele bir hatıra alacaksın. örn: 8 -> 8:00"
                    f"\n*Takvim*:"
                    f"\n{schedule}"
                )
            else:
                return (
                    f"{name}, your current schedule is below, You will get a random memory at each of these hours everyday. ie: 8 -> 8:00"
                    f"\n*Schedule*:"
                    f"\n{schedule}"
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
                    f"{name}, bu komutu bilmiyorum. Aşağıdaki komutları kullanabilirsin."
                    f"\n*schedule*"
                    f"\n*schedule add 8 12*"
                    f"\n*schedule reset*"
                    f"\n*schedule remove 8*"
                )
            else:
                return (
                    f"{name}, I do not know that command. You can support the commands below."
                    f"\n*schedule*"
                    f"\n*schedule add 8 12*"
                    f"\n*schedule reset*"
                    f"\n*schedule remove 8*"
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
        ) -> str:
            if language_code == "tr":
                if active:
                    is_active = "aktif"
                else:
                    is_active = "pasif"
                return (
                    f"Mevcut durumun:"
                    f"\n- Gmt: *GMT{gmt}*"
                    f"\n- Günlük gönderim aktif: *{is_active}*"
                    f"\n- Takvim: {schedule}"
                )
            else:
                return (
                    f"Your current status:"
                    f"\n- Gmt: *GMT{gmt}*"
                    f"\n- Daily sending is active: *{active}*"
                    f"\n- Schedule: {schedule}"
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
                    f"*gmt zaman-dilimi* ile zaman dilimi belirleyebilirsin, varsayılan zaman dilimi *GMT0*'dır. Bu arada Türkiye GMT+3 zaman diliminde."
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
                    f"Hatıra Kasana bir not(hatıra) eklemek için *add Cümle* komutunu kullanabilirsin."
                    f"\nÖrnek:"
                    f"\n*add Zaman çok kıymetlidir, her daim eriyen bir dondurmaya benzer.*"
                    f"\n\nBir sonraki rehber adımına geçmek için, /tutorial3"
                )
            else:
                return (
                    f"To add a note(memory) to your Memory Vault, please use the command, *add Sentence*."
                    f"\nExample:"
                    f"\n*add Time never does come back*"
                    f"\n\nFor the next tutorial step please use, /tutorial3"
                )

        @staticmethod
        def tutorial_3(name: str, language_code: str = "en"):
            if language_code == "tr":
                return (
                    f"\n- /leave veya *leave* ile günlük yollamayı durdurabilirsin"
                    f"\n- /send veya *send* ile rastgele bir hatıra yollarım"
                    f"\n- *send number* ile çok sayıda hatıra yollarım"
                    f"\n- /status veya *status* ile status bilgini yollarım"
                    f"\n- /list veya *list* ile tüm hatıralarını gönderirim"
                    f"\n\n{name} tebrikler rehberi bitirdin {Constants.smile}. Temel komutlarım bunlardı, günlük takvimi ayarlama vb. diğer komutları görmek için, /help."
                )

            else:
                return (
                    f"\n- /leave or *leave* to deactivate daily sending"
                    f"\n- /send or *send* to get a random memory"
                    f"\n- *send number* to get multiple random memories"
                    f"\n- /status or *status* to get your status information"
                    f"\n- /list or *list* to list memories"
                    f"\n\n{name} congratulations, you finished the tutorial {Constants.smile}. These were my main commands, to see additional commands like editing daily schedule please use, /help."
                )
