package com.song.model.mongomodel;

import org.hibernate.annotations.Type;
import org.springframework.data.mongodb.core.mapping.Document;

import javax.persistence.Entity;
import javax.persistence.Id;

import java.io.Serializable;
import java.util.Date;
import java.util.List;

import com.mongodb.util.JSON;
@Entity
@Document(collection="person")
public class MongoPosts {
    @Id
    private String id;
    private String name;
    //private int age;


    public String getId() {
        return id;
    }
    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    /*public int getAge() {
        return age;
    }
   public void setAge(int age) {
        this.age = age;
    }*/



}

