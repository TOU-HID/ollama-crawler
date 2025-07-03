import subprocess
import json

def extract_with_ollama(html: str) -> list[dict]:
    """
    Sends the HTML content to Ollama LLM and returns parsed JSON structured news articles.
    """

    # Prepare your prompt for Ollama
    prompt = f"""
			You are an intelligent content extractor. Given the raw HTML of a news page,
			extract news articles as JSON with fields: title, description, time, image, video.

			Return only valid JSON.

			HTML:
			```html
			{html}
			```"""

    # Run Ollama CLI as subprocess, send prompt to stdin and capture stdout
    try:
        process = subprocess.run(
            ["ollama", "run", "llama2"],  # replace "llama2" with your model name
            input=prompt.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        output = process.stdout.decode('utf-8').strip()

        # Debug print raw response (optional)
        print("🧠 Ollama raw response:")
        print(output)

        # Parse JSON from output
        data = json.loads(output)
        return data

    except subprocess.CalledProcessError as e:
        print(f"❌ Ollama subprocess failed: {e.stderr.decode()}")
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON from Ollama response: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    return []

