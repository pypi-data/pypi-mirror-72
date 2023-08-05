FROM taktile/base-serving-api:3463b64e3cb744fd10f79282c84f1390a6ab58f8
ENV APPDIR /app

# Install requirements
COPY ./requirements.txt ${APPDIR}/user_requirements.txt
RUN pip install -r ${APPDIR}/user_requirements.txt

# Copy code and assets for running the application
COPY ./src ${APPDIR}/src
COPY ./assets ${APPDIR}/assets

# Run model profile
RUN python ${APPDIR}/profile_endpoints.py
