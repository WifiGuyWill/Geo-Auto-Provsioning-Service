FROM python:alpine3.7
COPY ./src /app/src
COPY location_mapping.py /app
WORKDIR /app/src
RUN pip install -r requirements.txt
EXPOSE 5000
RUN chmod +x entrypoint.sh
ENTRYPOINT ["python", "app.py"]

#Set the Central data below before deploying the app
ENV USERNAME=xxxxxxxxxx@email.com
ENV PASSWORD=xxxxxxxxxx
ENV CLIENT_ID=xxxxxxxxxx
ENV CLIENT_SECRET=xxxxxxxxxx
ENV CUSTOMER_ID=xxxxxxxxxx
ENV BASE_URL=https://apigw-prod2.central.arubanetworks.com
ENV WEBHOOK_TOKEN=xxxxxxxxxx

#Central API base URLs:
#US-1 https://app1-apigw.central.arubanetworks.com
#US-2 https://apigw-prod2.central.arubanetworks.com
#US-WEST-4 https://apigw-uswest4.central.arubanetworks.com
#EU-1 https://eu-apigw.central.arubanetworks.com
#EU-3 https://apigw-eucentral3.central.arubanetworks.com
#Canada-1 https://apigw-ca.central.arubanetworks.com
#China-1 https://apigw.central.arubanetworks.com.cn
#APAC-1 https://api-ap.central.arubanetworks.com
#APAC-EAST1 https://apigw-apaceast.central.arubanetworks.com
#APAC-SOUTH1 https://apigw-apacsouth.central.arubanetworks.com