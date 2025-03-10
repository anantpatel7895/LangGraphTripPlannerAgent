import os
from dotenv import load_dotenv, find_dotenv



# load_dotenv("/Users/Anant/langgraph Agents/app/.env")

# Get the absolute path of the package
package_dir = os.path.dirname(os.path.abspath(__file__))

# print(package_dir)
# Load .env from package directory
load_dotenv(os.path.join(package_dir, ".env"))