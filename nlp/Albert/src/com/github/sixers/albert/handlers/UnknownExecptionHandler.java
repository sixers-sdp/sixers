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

import com.amazon.ask.dispatcher.exception.ExceptionHandler;
import com.amazon.ask.dispatcher.request.handler.HandlerInput;
import com.amazon.ask.exception.AskSdkException;
import com.amazon.ask.model.Response;

import java.util.Optional;

public class UnknownExecptionHandler implements ExceptionHandler {
    @Override
    public boolean canHandle(HandlerInput input, Throwable throwable) {
        return throwable instanceof AskSdkException;
    }

    @Override
    public Optional<Response> handle(HandlerInput input, Throwable throwable) {

        String exceptionType = throwable.getMessage();
        String tech_resp = "Human assistent is coming, please be patient";
        // TODO: DEAL WITH THE EXCEPTION.

        // TODO: DO A POST REQUEST TO THE API.
        return input.getResponseBuilder()
                .withSpeech(tech_resp)
                .build();

    }
}
