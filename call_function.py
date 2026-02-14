from google.genai import types
import functions
from functions import get_files_info

available_functions = types.Tool(
    function_declarations=[get_files_info.schema_get_files_info],
)
