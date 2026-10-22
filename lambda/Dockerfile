FROM public.ecr.aws/lambda/python:3.12

# copy amanzi and pyproject.toml, LICENSE and README.md
COPY amanzi ${LAMBDA_TASK_ROOT}/amanzi/
COPY pyproject.toml ${LAMBDA_TASK_ROOT}/amanzi/pyproject.toml
COPY LICENSE ${LAMBDA_TASK_ROOT}/amanzi/LICENSE
COPY README.md ${LAMBDA_TASK_ROOT}/amanzi/README.md
COPY VERSION ${LAMBDA_TASK_ROOT}/VERSION

# make ui folders (empty)
RUN mkdir -p ${LAMBDA_TASK_ROOT}/amanzi/ui
RUN mkdir -p ${LAMBDA_TASK_ROOT}/amanzi/ui/dist

# Install the specified packages
RUN pip install ${LAMBDA_TASK_ROOT}/amanzi

# Copy function code
COPY lambda/lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.handler" ]