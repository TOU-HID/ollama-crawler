import subprocess
import json
import re

def extract_with_ollama(html: str) -> list[dict]:
    """
    Extract structured news articles using Ollama.
    Only return JSON array parsed from the model's output.
    """

    prompt = f"""
			ONLY return a valid JSON array of news articles extracted from the following HTML.
			DO NOT explain. DO NOT use markdown. DO NOT provide code.

			Expected format:
			[
				{{
					"title": "...",
					"description": "...",
					"time": "...",
					"image": "...",
					"video": "..."
				}},
				...
			]

			Here is the HTML:
			{html}
			"""

    try:
        process = subprocess.run(
            ["ollama", "run", "mistral"],  # Replace with your model name
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        output = process.stdout.decode("utf-8").strip()

        print("🧠 Ollama raw response:")
        print(output)

        # Try to extract just the JSON array
        match = re.search(r"\[\s*{.*?}\s*\]", output, re.DOTALL)
        if match:
            json_str = match.group(0)
            return json.loads(json_str)

        print("❌ No valid JSON array found in Ollama output.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Ollama subprocess failed: {e.stderr.decode()}")
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON from Ollama response: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    return []
