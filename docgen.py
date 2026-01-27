import git 
from mistralai import Mistral
import os
from dotenv import load_dotenv 


def airesult(changes):
    prompt="this is the difference of code between commits explain me what changes is been done in the code and how it affects the logic give explanation as a documentation way"+changes
    mistral=Mistral(api_key=os.getenv("MISTRAL_API_KEY", ""),)
    
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
    file=open("document.txt","w")
    previouscommit=lastcommit.parents[0]

    diffs=previouscommit.diff(lastcommit,create_patch=True)
    count=1
    for i in diffs:
        content=(i.diff).decode("utf-8")
        doccontent=airesult(content)
        file.write("---CHANGE "+str(count)+"---")
        file.write(doccontent+"\n\n")
        count+=1
        file.flush()
   
    file.close()


def githookscript():
    if os.path.exists(".git/hooks/post-commit"):
        file=open(".git/hooks/post-commit","a")
        script=file.read()
        if "docgen.py" in script:
            codediff()
        else:
            file.write('\ncd "$(git rev-parse --show-toplevel)" || exit 0\npython3 docgen.py\nexit 0')
            file.close()

    else:
        file=open(".git/hooks/post-commit","a")
        file.write('#!/bin/bash\ncd "$(git rev-parse --show-toplevel)" || exit 0\npython3 docgen.py\nexit 0')
        file.close()




load_dotenv()
githookscript()
