import asyncio
from playwright.async_api import (
    async_playwright,
    TimeoutError as PlaywrightTimeoutError,
)
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

QUESTIONS = [
    "What is the capital of France?",
    "Who wrote 'To Kill a Mockingbird'?",
    "What is the square root of 64?",
    "What is the chemical formula for water?",
    "Who developed the theory of relativity?",
]

# XPath pattern for responses (using last() to get most recent answer)
RESPONSE_XPATH = "(//html/body/div[1]/main/div/div/div[2]/div/div/div/div/div[position() mod 2 = 1]/div/div/div[1])[last()]"


async def ask_question(page, question):
    """Process a single question and return the answer"""
    try:
        logger.info(f"Processing question: {question}")

        # Clear input and submit question
        textarea = await page.wait_for_selector(
            'textarea[placeholder="Ask anything..."]', timeout=15000
        )
        await textarea.fill("")  # Clear existing text
        await textarea.type(question, delay=100)  # Simulate human typing
        await textarea.press("Enter")

        # Wait fixed time for response
        logger.info("Waiting 10 seconds for response...")
        await asyncio.sleep(10)

        # Try to get response using XPath pattern
        response_element = await page.wait_for_selector(
            RESPONSE_XPATH, timeout=10000, state="attached"
        )

        # Scroll to ensure element is fully rendered
        await response_element.scroll_into_view_if_needed()

        # Get text and basic validation
        response = await response_element.inner_text()
        return response.strip() if response.strip() else "Empty response received"

    except PlaywrightTimeoutError:
        logger.warning("Response timeout occurred")
        await page.screenshot(path=f"timeout_{question[:10]}.png")
        return "Response timeout - answer not captured"
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        await page.screenshot(path=f"error_{question[:10]}.png")
        return f"Error: {str(e)}"


async def main():
    async with async_playwright() as p:
        logger.info("Launching browser...")
        browser = await p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled", "--start-maximized"],
            slow_mo=300,  # Slightly faster than previous but still visible
        )

        context = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        )

        page = await context.new_page()

        try:
            # Initial navigation
            await page.goto("https://labs.perplexity.ai/", wait_until="networkidle")
            await page.wait_for_selector(
                'textarea[placeholder="Ask anything..."]', state="visible"
            )

            # Process all questions
            answers = []
            for idx, question in enumerate(QUESTIONS):
                answer = await ask_question(page, question)
                answers.append(answer)

                print(f"\nQuestion {idx+1}: {question}")
                print(f"Answer: {answer}")
                print("=" * 80)

                # Add delay between questions
                if idx < len(QUESTIONS) - 1:
                    logger.info("Waiting 5 seconds before next question...")
                    await asyncio.sleep(5)

            return answers

        finally:
            await page.close()
            await context.close()
            await browser.close()


if __name__ == "__main__":
    results = asyncio.run(main())

    print("\nFinal Results:")
    for idx, (question, answer) in enumerate(zip(QUESTIONS, results)):
        print(f"{idx+1}. {question}")
        print(f"   {answer}\n")
