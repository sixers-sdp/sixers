/*
     Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.

     Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file
     except in compliance with the License. A copy of the License is located at

         http://aws.amazon.com/apache2.0/

     or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
     the specific language governing permissions and limitations under the License.
*/

package com.github.sixers.albert.handlers;

import com.amazon.ask.dispatcher.request.handler.HandlerInput;
import com.amazon.ask.dispatcher.request.handler.impl.IntentRequestHandler;
import com.amazon.ask.model.Intent;
import com.amazon.ask.model.IntentRequest;
import com.amazon.ask.model.Response;
import com.amazon.ask.model.Slot;
import org.apache.http.NameValuePair;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicNameValuePair;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import static com.amazon.ask.request.Predicates.intentName;

public class SetTableIntent implements IntentRequestHandler {

    @Override
    public boolean canHandle(HandlerInput handlerInput, IntentRequest intentRequest) {
        return (handlerInput.matches(intentName("SetTableIntent")));

    }

    @Override
    public Optional<Response> handle(HandlerInput handlerInput, IntentRequest intentRequest)  {
//
        Intent intent = intentRequest.getIntent();
        Slot tableNo = intent.getSlots().get("TableNUM");
        String tableNUM = tableNo.getValue();


        Slot password = intent.getSlots().get("password");
        String passwordValue = password.getValue();

        if (!passwordValue.equals(System.getenv("SetUpPW"))){
            return handlerInput.getResponseBuilder()
                    .withSpeech("This is an invalid password")
                    .build();
        }

        String deviceID = handlerInput.getRequestEnvelope().getContext().getSystem().getDevice().getDeviceId();


        CloseableHttpClient httpClient = HttpClients.createDefault();
        HttpPost httpPost = new HttpPost("http://albert.visgean.me/api/dots/");

        httpPost.addHeader("Authorization", System.getenv("API_TOKEN"));
        List<NameValuePair> nameValuePairs = new ArrayList<>();
        nameValuePairs.add(new BasicNameValuePair("dot_id", deviceID));
        nameValuePairs.add(new BasicNameValuePair("location", tableNUM));



        try {
            httpPost.setEntity(new UrlEncodedFormEntity(nameValuePairs, "UTF-8"));
            CloseableHttpResponse response = httpClient.execute(httpPost);
            httpClient.close();
        } catch (Exception e){
            e.printStackTrace();
        }


        return handlerInput.getResponseBuilder()
                .withSpeech("Set up confirmed.")
                .build();
    }

}