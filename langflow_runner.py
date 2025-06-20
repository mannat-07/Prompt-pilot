import argparse
import json
import logging 
from pathlib import Path 
import os
import requests
import warnings
from typing import Optional
from dotenv import load_dotenv
from argparse import RawTextHelpFormatter

# Optional import
try:
    from langflow.load import upload_file
except ImportError:
    warnings.warn("Langflow file upload not available. Install langflow for file upload support.")
    upload_file = None

# Load environment variables
load_dotenv()
load_dotenv(".env.local", override=True)

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = os.getenv("LANGFLOW_ID")
FLOW_ID = os.getenv("FLOW_ID")
APPLICATION_TOKEN = os.getenv("APPLICATION_TOKEN")

# Logging config
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 

# Default tweaks
DEFAULT_TWEAKS = {
    "AstraDBToolComponent-Dg6cx": {},
    "ParseData-r4Fhk": {},
    "GroqModel-ZMgtx": {},
    "ChatInput-D9hjW": {},
    "ChatOutput-ee0wn": {},
    "CombineText-SgCav": {}
}

def validate_env_vars():
    missing = []
    if not LANGFLOW_ID:
        missing.append("LANGFLOW_ID")
    if not FLOW_ID:
        missing.append("FLOW_ID")
    if not APPLICATION_TOKEN:
        missing.append("APPLICATION_TOKEN")

    if missing:
        raise EnvironmentError(
            f"Missing required environment variable(s): {', '.join(missing)}. "
            "Set them in your .env file or via command-line arguments."
        )


def run_flow(
    message: str,
    endpoint: str,
    output_type: str = "chat",
    input_type: str = "chat",
    tweaks: Optional[dict] = None,
    application_token: Optional[str] = None,
    verbose: bool = False
) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"
    headers = {
        "Authorization": f"Bearer {application_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type
    }

    if tweaks:
        payload["tweaks"] = tweaks

    if verbose:
        logger.debug(">>> Sending Request To: %s", api_url) 
        logger.debug(">>> Headers: %s", headers)
        logger.debug(">>> Payload: %s", json.dumps(payload, indent=2))

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": str(e)}


def main():
    epilog_text = """Examples:
  python langflow_runner.py "Hello!" --endpoint my_chat --application_token ABC123
  python langflow_runner.py "Analyze" --upload_file ./data.csv --components ParseData-r4Fhk --application_token ABC123
"""

    parser = argparse.ArgumentParser(
        description="Run a Langflow flow from the CLI with optional tweaks and file upload.",
        epilog=epilog_text,
        formatter_class=RawTextHelpFormatter
    )

    parser.add_argument("message", type=str, help="The message to send to the flow")
    parser.add_argument("--endpoint", type=str, default=FLOW_ID, help="Flow ID or custom endpoint name")
    parser.add_argument("--tweaks", type=str, default=json.dumps(DEFAULT_TWEAKS), help="Tweaks as JSON string")
    parser.add_argument("--application_token", type=str, default=APPLICATION_TOKEN, help="Your Langflow application token")
    parser.add_argument("--output_type", type=str, default="chat", help="Output type (default: chat)")
    parser.add_argument("--input_type", type=str, default="chat", help="Input type (default: chat)")
    parser.add_argument("--upload_file", type=str, help="Path to the file to upload (optional)")
    parser.add_argument("--components", type=str, help="Comma-separated list of component IDs to upload file to")
    parser.add_argument("--save_output", type=str, help="Save the response to this file (optional)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose/debug output")
    parser.add_argument("--raw", action="store_true", help="Print raw JSON without formatting") 

    args = parser.parse_args()

    # Environment token validation
    if not args.application_token or "<YOUR_APPLICATION_TOKEN>" in args.application_token:
        raise ValueError("❌ Please set your actual APPLICATION_TOKEN via --application_token or .env file")

    if not args.endpoint:
        raise ValueError("Missing flow ID. Please provide --endpoint or set FLOW_ID in your .env file.") 

    try:
        tweaks = json.loads(args.tweaks)
    except json.JSONDecodeError:
        raise ValueError("Invalid tweaks JSON string")

    # Validate environment variables (used only if not passed via args)
    validate_env_vars() 

    # Handle file upload
    if args.upload_file:
        if not upload_file:
            raise ImportError("Langflow is not installed. Install it with: pip install langflow")

        file_path = Path(args.upload_file) 
        if not file_path.is_file():  
            raise FileNotFoundError(f"❌ File '{args.upload_file}' does not exist.") 

        if not args.components:
            raise ValueError("You must provide --components to upload a file")

        components_list = [c.strip() for c in args.components.split(",")]
        tweaks = upload_file(
            file_path=str(file_path),
            host=BASE_API_URL,
            flow_id=args.endpoint,
            components=components_list,
            tweaks=tweaks
        )

    # Run the flow
    response = run_flow(
        message=args.message,
        endpoint=args.endpoint,
        output_type=args.output_type,
        input_type=args.input_type,
        tweaks=tweaks,
        application_token=args.application_token,
        verbose=args.verbose
    )

    # Output response
    if args.raw:
        print(json.dumps(response)) 
    else:
        print(json.dumps(response, indent=2))

    # Save output if requested
    if args.save_output:
        try:
            with open(args.save_output, "w") as f:
                json.dump(response, f, indent=2)
            print(f"✅ Output saved to {args.save_output}")
        except IOError as e:
            print(f"❌ Failed to save output: {e}")

if __name__ == "__main__":
    main()
