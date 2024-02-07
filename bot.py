from modules.main_bot_module.main_module import Main_Module



bot = Main_Module()
bot.manage_database_creation()
try:
    while True:
        bot.chatbot()
        pass
except KeyboardInterrupt:
    print("\n\nCtrl+C detected. Exiting gracefully...\n\n")
    quit()

