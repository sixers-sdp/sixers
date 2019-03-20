package com.github.sixers.albert.query;

import java.util.HashMap;

public class Order {

    HashMap<String,Integer> orders;

    public Order(){
        orders = new HashMap<>();
    }


    public void addProduct(String name, Integer num){

        orders.put(name,orders.getOrDefault(name,0) + num);

    }

    public String toString(){

        String ans = new String();
        for(String st: orders.keySet()){
            ans = ans + st + ":" + orders.get(st) +"/";
        }return ans;
    }

}
