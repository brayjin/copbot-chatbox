import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from CopBotChatbox.database import initialize_db
if __name__ == "__main__":
    initialize_db()
    print("Database initialized!")
