package com.github.sixers.albert.handlers;

import com.amazon.ask.dispatcher.exception.ExceptionHandler;
import com.amazon.ask.dispatcher.request.handler.HandlerInput;
import com.amazon.ask.model.Response;
import com.github.sixers.albert.exception.HumanNeededException;
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

public class HumanNeededExecptionHandler implements ExceptionHandler {
    @Override
    public boolean canHandle(HandlerInput input, Throwable throwable) {
        return throwable instanceof HumanNeededException;
    }

    @Override
    public Optional<Response> handle(HandlerInput input, Throwable throwable) {


        String resp = "Human assistant is coming, please be patient";
        String message = throwable.getMessage();

        CloseableHttpClient httpClient = HttpClients.createDefault();
        String deviceID = input.getRequestEnvelope().getContext().getSystem().getDevice().getDeviceId();


        // TODO: DO A POST REQUEST TO THE API.
        HttpPost httpPost = new HttpPost("http://albert.visgean.me/api/human_requests/");
        httpPost.addHeader("Authorization", System.getenv("API_TOKEN"));
        List<NameValuePair> nameValuePairs = new ArrayList<>();
        nameValuePairs.add(new BasicNameValuePair("device_id", deviceID));
        // TODO: Should be Modified to adapted new API.
        nameValuePairs.add(new BasicNameValuePair("text", message));

        try {
            httpPost.setEntity(new UrlEncodedFormEntity(nameValuePairs, "UTF-8"));
            CloseableHttpResponse response = httpClient.execute(httpPost);
            httpClient.close();
        } catch (Exception e) {
            e.printStackTrace();
        }

        return input.getResponseBuilder()
                .withSpeech(resp)
                .build();
    }
}