"""Build verified full and standalone ZIPs with checksums."""
from pathlib import Path
import hashlib,zipfile
ROOT=Path(__file__).resolve().parents[1]
for root,name in [(ROOT,'OpenVals_Research_Publication_Package.zip'),(ROOT/'case-study-003-prompt-injection','OpenVals_Case_Study_003.zip')]:
    files=sorted(p for p in root.rglob('*') if p.is_file() and not any(x in {'.git','__pycache__','.DS_Store'} for x in p.relative_to(root).parts) and p.suffix not in {'.pyc','.zip'})
    output=ROOT.parent/name
    manifest=''
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
        for p in files:
            rel=p.relative_to(root).as_posix()
            z.write(p,root.name+'/'+rel)
            manifest+=hashlib.sha256(p.read_bytes()).hexdigest()+'  '+rel+'\n'
        z.writestr(root.name+'/SHA256SUMS.txt',manifest)
    with zipfile.ZipFile(output) as z:
        assert z.testzip() is None
        for p in files:assert z.read(root.name+'/'+p.relative_to(root).as_posix())==p.read_bytes()
    output.with_suffix('.zip.sha256').write_text(hashlib.sha256(output.read_bytes()).hexdigest()+'  '+name+'\n')
    print('Verified',output)
