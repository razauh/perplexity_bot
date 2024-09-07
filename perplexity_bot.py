import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from playwright.async_api import (
    async_playwright,
    TimeoutError as PlaywrightTimeoutError,
    Error as PlaywrightError,
)
import logging

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


# Define the request model for the API endpoint
class QueryRequest(BaseModel):
    question: str


async def fetch_response(question: str):
    try:
        # Use Playwright to interact with the webpage
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(
                headless=True
            )  # Use headless=True for server environments
            page = await browser.new_page()

            # Attempt to navigate to the target page
            try:
                await page.goto(
                    "https://labs.perplexity.ai/", timeout=30000
                )  # 30 seconds timeout for page load
            except PlaywrightTimeoutError:
                logger.error("Timeout while loading the target webpage.")
                raise HTTPException(
                    status_code=504, detail="Timeout while loading the target webpage."
                )

            # Attempt to fill in the question and fetch the response
            try:
                await page.fill('//textarea[@placeholder="Ask anything..."]', question)
                await page.press('//textarea[@placeholder="Ask anything..."]', "Enter")
                await page.wait_for_timeout(25000)  # Wait for the response

                response = None
                for attempt in range(3):  # Retry logic
                    try:
                        response_element = await page.wait_for_selector(
                            "(//html/body/div[1]/main/div/div/div[2]/div/div/div/div/div[position() mod 2 = 1]/div/div/div[1])[last()]",
                            state="attached",
                            timeout=60000,
                        )
                        await response_element.scroll_into_view_if_needed()
                        response = await response_element.inner_text()
                        break
                    except PlaywrightTimeoutError:
                        logger.warning(
                            f"Attempt {attempt + 1} failed: Timeout exceeded. Retrying..."
                        )

                if response is None:
                    await page.screenshot(path="error_screenshot.png")
                    content = await page.content()
                    logger.error(
                        f"Failed to retrieve the response after multiple attempts. HTML content at timeout: {content}"
                    )
                    raise HTTPException(
                        status_code=502,
                        detail="Failed to retrieve the response from the webpage.",
                    )

                return response

            except PlaywrightError as e:
                logger.error(f"Error while interacting with the page: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Error while interacting with the page: {str(e)}",
                )

    except PlaywrightError as e:
        logger.error(
            f"Error launching the browser or other Playwright issues: {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail=f"Error launching the browser or other Playwright issues: {str(e)}",
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


@app.post("/ask")
async def ask_question(query: QueryRequest):
    response = await fetch_response(query.question)
    return {"response": response}


@app.get("/")
async def read_root():
    return {"message": "Welcome to the generalized FastAPI for interactive Q&A!"}
