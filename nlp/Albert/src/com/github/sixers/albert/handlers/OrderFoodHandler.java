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

public class OrderFoodHandler implements IntentRequestHandler {

    @Override
    public boolean canHandle(HandlerInput handlerInput, IntentRequest intentRequest) {
        return (handlerInput.matches(intentName("OrderFood")));

    }

    @Override
    public Optional<Response> handle(HandlerInput handlerInput, IntentRequest intentRequest)  {
//
        Intent intent = intentRequest.getIntent();
        Slot food = intent.getSlots().get("Food");
        //Slot number = intent.getSlots().get("Number");
//
        String foodName = food.getResolutions().getResolutionsPerAuthority().get(0).getValues().get(0).getValue().getName();
//        String foodNumber = number.getResolutions().getResolutionsPerAuthority().get(0).getValues().get(0).getValue().getName();

//        String speechText = "You order " + foodNumber +" " + foodName;

//        CloseableHttpClient httpClient = HttpClients.createDefault();
//        HttpPost httpPost = new HttpPost("http://albert.visgean.me/api/orders/");
//        List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();
//        nameValuePairs.add(new BasicNameValuePair("Number", foodNumber));
//        nameValuePairs.add(new BasicNameValuePair("Name", foodName));
//        try {
//            httpPost.setEntity(new UrlEncodedFormEntity(nameValuePairs, "UTF-8"));
//            CloseableHttpResponse response = httpClient.execute(httpPost);
//            httpClient.close();
//        } catch (Exception e){
//            e.printStackTrace();
//        }

        //String foodName = food.getValue();
        //String foodNumber = number.getValue();
        String speechText = "You order " + foodName;

        CloseableHttpClient httpClient = HttpClients.createDefault();
        HttpPost httpPost = new HttpPost("http://albert.visgean.me/api/orders/");
        List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();
        //nameValuePairs.add(new BasicNameValuePair("Number", foodNumber));
        nameValuePairs.add(new BasicNameValuePair("table_number", "t1"));
        nameValuePairs.add(new BasicNameValuePair("state", "new"));
        nameValuePairs.add(new BasicNameValuePair("products_text", foodName));
        try {
            httpPost.setEntity(new UrlEncodedFormEntity(nameValuePairs, "UTF-8"));
            CloseableHttpResponse response = httpClient.execute(httpPost);
            httpClient.close();
        } catch (Exception e){
            e.printStackTrace();
        }

        return handlerInput.getResponseBuilder()
                .withSpeech(speechText)
                .build();
    }

}
