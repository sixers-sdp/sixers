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

public class CancelDrinkHandler implements IntentRequestHandler {

	@Override
	public boolean canHandle(HandlerInput handlerInput, IntentRequest intentRequest) {
		return (handlerInput.matches(intentName("CancelDrink")));

	}

	@Override
	public Optional<Response> handle(HandlerInput handlerInput, IntentRequest intentRequest) {

		Intent intent = intentRequest.getIntent();
		// Drink names
		Slot drinkone = intent.getSlots().get("Drinkone");
		Slot drinktwo = intent.getSlots().get("Drinktwo");
		Slot drinkthree = intent.getSlots().get("Drinkthree");

		// Number
		Slot numone = intent.getSlots().get("Numberone");
		Slot numtwo = intent.getSlots().get("Numbertwo");
		Slot numthree = intent.getSlots().get("Numberthree");

		// defining default value for strings
		String drinktwoName = "";
		String drinkthreeName = "";

		String numoneValue = "one";
		String numtwoValue = "one";
		String numthreeValue = "one";

		// Checking slot values and assign the corresponding string value

		// ordered drink name

		String drinkoneName = drinkone.getResolutions().getResolutionsPerAuthority().get(0).getValues().get(0)
				.getValue().getName();

		if (drinktwo.getValue() != null) {
			drinktwoName = drinktwo.getResolutions().getResolutionsPerAuthority().get(0).getValues().get(0).getValue()
					.getName();
		}
		if (drinkthree.getValue() != null) {
			drinkthreeName = drinkthree.getResolutions().getResolutionsPerAuthority().get(0).getValues().get(0)
					.getValue().getName();
		}

		if (numone.getValue() != null) {
			numoneValue = numone.getResolutions().getResolutionsPerAuthority().get(0).getValues().get(0).getValue()
					.getName();
		}
		if (numtwo.getValue() != null) {
			numtwoValue = numtwo.getResolutions().getResolutionsPerAuthority().get(0).getValues().get(0).getValue()
					.getName();
		}
		if (numthree.getValue() != null) {
			numthreeValue = numthree.getResolutions().getResolutionsPerAuthority().get(0).getValues().get(0).getValue()
					.getName();
		}

		String deviceID = handlerInput.getRequestEnvelope().getContext().getSystem().getDevice().getDeviceId();

		// Construct respond text
		String speechText = "You have cancelled ";
		speechText = speechText + numoneValue + " " + drinkoneName;
		if (!drinktwoName.equals("")) {
			if (drinkthreeName.equals("")) {
				speechText = speechText + " and " + numtwoValue + " " + drinktwoName;
			} else {
				speechText = speechText + ", " + numtwoValue + " " + drinktwoName;
				speechText = speechText + " and " + numthreeValue + " " + drinkthreeName;
			}
		}

		if (intent.getConfirmationStatus().getValue().toString().equals("CONFIRMED")) {

			CloseableHttpClient httpClient = HttpClients.createDefault();
			HttpPost httpPost = new HttpPost("http://albert.visgean.me/api/orders/");

			httpPost.addHeader("Authorization", System.getenv("API_TOKEN"));
			List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();
			nameValuePairs.add(new BasicNameValuePair("device_id", deviceID));
			// TODO: Should be Modified to adapted new API.
			nameValuePairs.add(new BasicNameValuePair("products_text", speechText));

			try {
				httpPost.setEntity(new UrlEncodedFormEntity(nameValuePairs, "UTF-8"));
				CloseableHttpResponse response = httpClient.execute(httpPost);
				httpClient.close();
			} catch (Exception e) {
				e.printStackTrace();
			}

			return handlerInput.getResponseBuilder().withSpeech(speechText)
					.withReprompt("Would you like to order something else?").withShouldEndSession(false).build();
		} else {
			return handlerInput.getResponseBuilder()
					.withSpeech("Okay, I have not cancelled your order. Would you like to cancel something else?")
					.withReprompt("Would you like to order anything else?").withShouldEndSession(false).build();
		}

	}
}