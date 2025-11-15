import PyPDF2
from agents import function_tool

def _resume_parser_impl(file_path: str) -> dict:
    """
    Local callable implementation for resume_parser tool.
    Used when calling the parser outside of agent runtime.
    """
    extracted_info = {
        "name": "",
        "email": "",
        "phone": "",
        "education": [],
        "experience": [],
        "skills": []
    }

    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text() + "\n"

            lines = full_text.splitlines()
            for line in lines:
                line = line.strip()
                if "Name:" in line:
                    extracted_info["name"] = line.split("Name:")[1].strip()
                elif "Email:" in line:
                    extracted_info["email"] = line.split("Email:")[1].strip()
                elif "Phone:" in line:
                    extracted_info["phone"] = line.split("Phone:")[1].strip()
                elif "Education:" in line:
                    extracted_info["education"].append(line.split("Education:")[1].strip())
                elif "Experience:" in line:
                    extracted_info["experience"].append(line.split("Experience:")[1].strip())
                elif "Skills:" in line:
                    skills = line.split("Skills:")[1].strip().split(',')
                    extracted_info["skills"].extend([skill.strip() for skill in skills])
    except Exception as e:
        extracted_info["error"] = str(e)

    return extracted_info


@function_tool
def resume_parser(file_path: str) -> dict:
    """Agent-accessible function tool wrapper."""
    return _resume_parser_impl(file_path)



def _pdf_extractor_impl(file_path: str, page_numbers: list[int]) -> str:
    """Actual PDF extraction implementation."""
    extracted_text = []
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in page_numbers:
            if 0 <= page_num < len(reader.pages):
                page = reader.pages[page_num]
                extracted_text.append(page.extract_text() or "")
            else:
                extracted_text.append(f"Page {page_num} is out of range.")
    return "\n".join(extracted_text)


@function_tool
def pdf_extractor(file_path: str, page_numbers: list[int]) -> str:
    """Wrapped FunctionTool version for agents."""
    return _pdf_extractor_impl(file_path, page_numbers)