rm -rf codeql/db

codeql database create codeql/db -l python -s app

codeql database analyze codeql/db codeql/python-queries:codeql-suites/python-security-and-quality.qls \
    --format=csv \
    --output=codeql/cocktail-maker-security-and-quality-$(date +%Y%m%d_%H%M%S).csv \
    --download

codeql database analyze codeql/db codeql/python-queries:codeql-suites/python-security-and-quality.qls \
    --format=sarif-latest \
    --output=codeql/cocktail-maker-security-and-quality-$(date +%Y%m%d_%H%M%S).sarif.json \
    --download && \
    cd codeql && \
    npx prettier *.sarif.json --write
