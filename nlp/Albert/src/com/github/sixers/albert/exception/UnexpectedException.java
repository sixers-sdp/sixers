package com.github.sixers.albert.exception;

import com.amazon.ask.exception.AskSdkException;

public class UnexpectedException extends AskSdkException {

    public UnexpectedException(String message) {
        super(message);
    }

    public UnexpectedException(String message, Throwable cause) {
        super(message, cause);
    }

}