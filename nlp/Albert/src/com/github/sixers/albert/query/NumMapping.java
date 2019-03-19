package com.github.sixers.albert.query;

public class NumMapping {

    public static Integer numMapping(String st){

        if(st.equals("one")){
            return 1;
        }
        if(st.equals("two")){
            return 2;
        }
        if(st.equals("three")){
            return 3;
        }
        if (st.equals("four")){
            return 4;
        }
        if(st.equals("five")){
            return 5;
        }
        if (st.equals("six")){
            return 6;
        }

        return 1;


    }

}
