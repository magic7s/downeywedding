# downeywedding
[![pipeline status](https://gitlab.com/bdowney/downeywedding/badges/master/pipeline.svg)](https://gitlab.com/bdowney/downeywedding/commits/master)


## LAMBDA FUNCTION
AWS Lambda requires that all libraries are in a .zip file AT THE ROOT level.

See http://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html

```
pip install gspread oauth2client -t ./project-dir
cp lambda_function.py ./project-dir
cp GoogleSheetAPI-OAUTH2.json ./project-dir
cd project-dir;zip -r ../mylambdafunction.zip ./ -x \*.pyc ; cd ..
```
