package com.amazon.ask.helloworld.query;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.Map;

public class httpHelper {

    /**
     * 获取接口返回的结果(POST).
     *
     * @param postUrl          请求接口的url
     * @param requestParam     请求接口的参数
     * @param requestHeader    请求接口的Header
     * @return 请求接口的返回值
     * @throws IOException the io exception
     */
    public static String getResponseMess(String postUrl, Map<Object, Object> requestParam, Map<Object, Object> requestHeader) throws IOException {
        URL url = new URL(postUrl);
        // 将url 以 open方法返回的urlConnection  连接强转为HttpURLConnection连接  (标识一个url所引用的远程对象连接)
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();// 此时cnnection只是为一个连接对象,待连接中
        // 设置连接输出流为true,默认false (post 请求是以流的方式隐式的传递参数)
        connection.setDoOutput(true);
        // 设置连接输入流为true
        connection.setDoInput(true);
        // 设置请求方式为post
        connection.setRequestMethod("POST");
        // post请求缓存设为false
        connection.setUseCaches(false);
        // 设置该HttpURLConnection实例是否自动执行重定向
        connection.setInstanceFollowRedirects(true);

        if (requestHeader != null) {
            // 设置 Header 信息
            for (Map.Entry<Object, Object> entry : requestHeader.entrySet()) {
                connection.setRequestProperty(entry.getKey().toString(), entry.getValue().toString());
            }
        }
        connection.connect();//建立连接

        DataOutputStream outputStream = new DataOutputStream(connection.getOutputStream());
        String param = "";
        if (requestParam != null) {
            for (Map.Entry<Object, Object> entry : requestParam.entrySet()) {
                if ("".equals(param) || param == "") {
                    param = entry.getKey() + "=" + URLEncoder.encode(entry.getValue().toString(), "utf-8");
                } else {
                    param = param + "&" + entry.getKey() + "=" +URLEncoder.encode( entry.getValue().toString(), "utf-8");
                }
            }
        }
        outputStream.writeBytes(param);

        outputStream.flush();
        outputStream.close();

        // 连接发起请求,处理服务器响应  (从连接获取到输入流并包装为bufferedReader)
        BufferedReader bf = new BufferedReader(new InputStreamReader(connection.getInputStream(), "UTF-8"));
        String line;
        StringBuilder sb = new StringBuilder();
        // 循环读取流,若不到结尾处
        while ((line = bf.readLine()) != null) {
            sb.append(line).append(System.getProperty("line.separator"));
        }
        bf.close();    // 关闭流
        connection.disconnect(); // 销毁连接

        return sb.toString();
    }
}
