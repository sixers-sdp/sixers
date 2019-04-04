package com.github.sixers.albert.handlers;

import com.amazon.ask.dispatcher.exception.ExceptionHandler;
import com.amazon.ask.dispatcher.request.handler.HandlerInput;
import com.amazon.ask.model.Response;
import com.github.sixers.albert.exception.HumanNeededException;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;

import java.util.Optional;

public class HumanNeededExecptionHandler implements ExceptionHandler {
    @Override
    public boolean canHandle(HandlerInput input, Throwable throwable) {
        return throwable instanceof HumanNeededException;
    }

    @Override
    public Optional<Response> handle(HandlerInput input, Throwable throwable) {


        String resp = "Human assistant is coming, please be patient";

        CloseableHttpClient httpClient = HttpClients.createDefault();

        // TODO: DO A POST REQUEST TO THE API.
        HttpPost httpPost = new HttpPost("http://albert.visgean.me/api/");
        httpPost.addHeader("Authorization", System.getenv("API_TOKEN"));

        return input.getResponseBuilder()
                .withSpeech(resp)
                .build();
    }
}
