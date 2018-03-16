package com.song.model.mysqlmodel;

import javax.persistence.*;
import java.io.Serializable;

@Entity
@NamedQuery(name="users.deleteUser", query="delete from User u where u.id = :id")
@Table(name="Users")
public class User implements Serializable {

	@Id
	@GeneratedValue(strategy = GenerationType.AUTO)
	private int id;
	
	@Column(nullable=false,unique=true)
	private String email;
	@Column(nullable=false)
	private String password;

	public User() {}

	public User(String email, String password) {
		super();
		this.email = email;
		this.password = password;

	}

	public String getEmail() {
		return email;
	}

	public void setEmail(String email) {
		this.email = email;
	}

	public void setPassword(String password) {
		this.password = password;
	}

	public String getPassword() {
		return password;
	}
	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}
}
