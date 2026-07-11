import sys
import json
import urllib.request
import xml.etree.ElementTree as ET


def search_arxiv(query, max_results=5):
    url = f"http://export.arxiv.org/api/query?search_query=all:{urllib.parse.quote(query)}&max_results={max_results}&sort=submittedDate&sortOrder=descending"
    try:
        response = urllib.request.urlopen(url)
        xml_data = response.read()
        root = ET.fromstring(xml_data)

        results = []
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            title = (entry.find(
                "{http://www.w3.org/2005/Atom}title").text.strip().replace(
                    "\n", " "))
            summary = (entry.find(
                "{http://www.w3.org/2005/Atom}summary").text.strip().replace(
                    "\n", " "))
            published = entry.find(
                "{http://www.w3.org/2005/Atom}published").text[:10]
            authors = [
                a.find("{http://www.w3.org/2005/Atom}name").text
                for a in entry.findall("{http://www.w3.org/2005/Atom}author")
            ]

            results.append({
                "title": title,
                "authors": ", ".join(authors),
                "published": published,
                "summary": summary,
            })
        print(json.dumps(results, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))


if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "Large Language Models"
    search_arxiv(query)
