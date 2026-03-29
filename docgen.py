import git 
from mistralai.client import Mistral
import os
from datetime import datetime


# PASTE API KEY BELOW

apikey=""



def airesult(changes):
    prompt="this is the difference of code between commits explain me what changes is been done in the code and how it affects the logic give explanation as a documentation way"+changes
    mistral=Mistral(api_key=apikey,)
    
    res = mistral.chat.complete(model="mistral-small-latest", messages=[
        {
            "content": prompt,
            "role": "user",
        },
    ], stream=False)

    
    return res.choices[0].message.content

def codediff():

    repo=git.Repo(os.getcwd())

    lastcommit=repo.head.commit 
    file=open("document.txt","a")
    previouscommit=lastcommit.parents[0]

    
    diffs=previouscommit.diff(lastcommit,create_patch=True)
    count=1


    timenow=datetime.now()
    datetimestr=timenow.strftime("%Y-%m-%d %H:%M:%S")
    file.write("-"*7+datetimestr+"-"*7+"\n\n")
    file.flush()
    for i in diffs:
        content=(i.diff).decode("utf-8")
        doccontent=airesult(content)
        file.write("---CHANGE "+str(count)+"---\n")
        file.write(doccontent+"\n\n")
        count+=1
        file.flush()
   
    file.close()


def githubpipeline():
    if os.path.exists(".github/workflows/docgen.yml"):
        codediff()

    else:
        os.makedirs(".github/workflows/",exist_ok=True)
        file=open(".github/workflows/docgen.yml","a")
        pipelineyml = "name: Doc Generator Pipeline\n\non:\n  push:\n\npermissions:\n  contents: write\n\njobs:\n  generate-docs:\n    runs-on: ubuntu-latest\n\n    steps:\n      - name: Checkout repository\n        uses: actions/checkout@v3\n        with:\n          fetch-depth: 0\n\n      - name: Set up Python\n        uses: actions/setup-python@v4\n        with:\n          python-version: '3.10'\n\n      - name: Install dependencies\n        run: |\n          pip install -r requirements.txt\n\n      - name: Run doc generator\n        run: |\n          python docgen.py\n\n      - name: Commit generated docs\n        run: |\n          git config user.name \"github-actions\"\n          git config user.email \"actions@github.com\"\n          git add *.txt\n          git commit -m \"Auto-generated docs [skip ci]\" || echo \"No changes to commit\"\n          git push origin HEAD:${{ github.ref }}\n"
        file.write(pipelineyml)
        file.close()





githubpipeline()
