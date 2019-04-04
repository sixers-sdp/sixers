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

public class CancelFoodHandler implements IntentRequestHandler {

	@Override
	public boolean canHandle(HandlerInput handlerInput, IntentRequest intentRequest) {
		return (handlerInput.matches(intentName("CancelFood")));

	}

	@Override
	public Optional<Response> handle(HandlerInput handlerInput, IntentRequest intentRequest) {
//

		Intent intent = intentRequest.getIntent();
		// Food names
		Slot foodone = intent.getSlots().get("Foodone");
		Slot foodtwo = intent.getSlots().get("Foodtwo");
		Slot foodthree = intent.getSlots().get("Foodthree");

		// Number
		Slot numone = intent.getSlots().get("Numberone");
		Slot numtwo = intent.getSlots().get("Numbertwo");
		Slot numthree = intent.getSlots().get("Numberthree");

		// defining default value for strings
		String foodtwoName = "";
		String foodthreeName = "";

		String numoneValue = "one";
		String numtwoValue = "one";
		String numthreeValue = "one";

		// Checking slot values and assign the corresponding string value

		// ordered food name
		String foodoneName = foodone.getResolutions().getResolutionsPerAuthority().get(0).getValues().get(0).getValue()
				.getName();
		if (foodtwo.getValue() != null) {
			foodtwoName = foodtwo.getResolutions().getResolutionsPerAuthority().get(0).getValues().get(0).getValue()
					.getName();
		}
		if (foodthree.getValue() != null) {
			foodthreeName = foodthree.getResolutions().getResolutionsPerAuthority().get(0).getValues().get(0).getValue()
					.getName();
		}

		// ordered number value of food
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
		//Construct chef's order string
		String chefText = "CANCELLATION: ";
		speechText = speechText + numoneValue + " " + foodoneName;
		if (numoneValue.equals("one")){
			chefText = chefText + "1x " +foodoneName + "\n";
		}
		else if (numoneValue.equals("two")){
			chefText = chefText + "2x " +foodoneName + "\n";
		}
		else if (numoneValue.equals("three")){
			chefText = chefText + "3x " +foodoneName + "\n";
		}
		else if (numoneValue.equals("four")){
			chefText = chefText + "4x " +foodoneName + "\n";
		}
		else if (numoneValue.equals("five")){
			chefText = chefText + "5x " +foodoneName + "\n";
		}
		else if (numoneValue.equals("six")){
			chefText = chefText + "6x " +foodoneName + "\n";
		}
		else if (numoneValue.equals("seven")){
			chefText = chefText + "7x " +foodoneName + "\n";
		}
		else if (numoneValue.equals("eight")){
			chefText = chefText + "8x " +foodoneName + "\n";
		}
		else if (numoneValue.equals("nine")){
			chefText = chefText + "9x " +foodoneName + "\n";
		}
		if (!foodtwoName.equals("")) {
			if (numtwoValue.equals("one")){
				chefText = chefText + "1x " +foodtwoName + "\n";
			}
			else if (numtwoValue.equals("two")){
				chefText = chefText + "2x " +foodtwoName + "\n";
			}
			else if (numtwoValue.equals("three")){
				chefText = chefText + "3x " +foodtwoName + "\n";
			}
			else if (numtwoValue.equals("four")){
				chefText = chefText + "4x " +foodtwoName + "\n";
			}
			else if (numtwoValue.equals("five")){
				chefText = chefText + "5x " +foodtwoName + "\n";
			}
			else if (numtwoValue.equals("six")){
				chefText = chefText + "6x " +foodtwoName + "\n";
			}
			else if (numoneValue.equals("seven")){
				chefText = chefText + "7x " +foodtwoName + "\n";
			}
			else if (numoneValue.equals("eight")){
				chefText = chefText + "8x " +foodtwoName + "\n";
			}
			else if (numoneValue.equals("nine")){
				chefText = chefText + "9x " +foodtwoName + "\n";
			}
			if (foodthreeName.equals("")) {
				speechText = speechText + " and " + numtwoValue + " " + foodtwoName;
			} else {
				speechText = speechText + ", " + numtwoValue + " " + foodtwoName;
				speechText = speechText + " and " + numthreeValue + " " + foodthreeName;
				if (numthreeValue.equals("one")){
					chefText = chefText + "1x " +foodthreeName + "\n";
				}
				else if (numthreeValue.equals("two")){
					chefText = chefText + "2x " +foodthreeName + "\n";
				}
				else if (numthreeValue.equals("three")){
					chefText = chefText + "3x " +foodthreeName + "\n";
				}
				else if (numthreeValue.equals("four")){
					chefText = chefText + "4x " +foodthreeName + "\n";
				}
				else if (numthreeValue.equals("five")){
					chefText = chefText + "5x " +foodthreeName + "\n";
				}
				else if (numthreeValue.equals("six")){
					chefText = chefText + "6x " +foodthreeName + "\n";
				}
				else if (numoneValue.equals("seven")){
					chefText = chefText + "7x " +foodthreeName + "\n";
				}
				else if (numoneValue.equals("eight")){
					chefText = chefText + "8x " +foodthreeName + "\n";
				}
				else if (numoneValue.equals("nine")){
					chefText = chefText + "9x " +foodthreeName + "\n";
				}
			}
		}

		if (!foodtwoName.equals("")) {
			if (foodthreeName.equals("")) {
				speechText = speechText + " and " + numtwoValue + " " + foodtwoName;
			} else {
				speechText = speechText + ", " + numtwoValue + " " + foodtwoName;
				speechText = speechText + " and " + numthreeValue + " " + foodthreeName;
			}
		}

		if (intent.getConfirmationStatus().getValue().toString().equals("CONFIRMED")) {

			CloseableHttpClient httpClient = HttpClients.createDefault();
			HttpPost httpPost = new HttpPost("http://albert.visgean.me/api/cancel/");

			httpPost.addHeader("Authorization", System.getenv("API_TOKEN"));
			List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();
			nameValuePairs.add(new BasicNameValuePair("device_id", deviceID));
			// TODO: Should be Modified to adapted new API.
			nameValuePairs.add(new BasicNameValuePair("text", chefText));

			try {
				httpPost.setEntity(new UrlEncodedFormEntity(nameValuePairs, "UTF-8"));
				CloseableHttpResponse response = httpClient.execute(httpPost);
				httpClient.close();
			} catch (Exception e) {
				e.printStackTrace();
			}

			return handlerInput.getResponseBuilder().withSpeech(speechText)
					.withReprompt("What else can I do for you").withShouldEndSession(false).build();
		} else {
			return handlerInput.getResponseBuilder()
					.withSpeech("Okay, I have not cancelled your order. What else can I do for you?")
					.withReprompt("What else can I do for you?").withShouldEndSession(false).build();
		}

	}
}
