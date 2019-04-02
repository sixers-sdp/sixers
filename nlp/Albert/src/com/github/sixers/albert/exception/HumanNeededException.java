package com.github.sixers.albert.exception;

import com.amazon.ask.exception.AskSdkException;

public class HumanNeededException extends AskSdkException {

    public HumanNeededException(String message) {
        super(message);
    }

    public HumanNeededException(String message, Throwable cause) {
        super(message, cause);
    }
}
