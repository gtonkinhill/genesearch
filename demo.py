import asyncio
from EdgeGPT import Chatbot, ConversationStyle


# export COOKIE_FILE=/Users/gt4/Downloads/edgeGPT/cookies.json

async def main():
    bot = Chatbot()
    print(await bot.ask(prompt="Hello world", 
                        conversation_style=ConversationStyle.creative, 
                        wss_link="wss://sydney.bing.com/sydney/ChatHub"))
    await bot.close()


if __name__ == "__main__":
    asyncio.run(main())