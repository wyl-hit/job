package com.song.model.mysqlmodel;

import javax.persistence.*;
import java.io.Serializable;

@Entity
@Table(name="Reply_task")
public class ReplyTask implements Serializable {

	@Id
	@GeneratedValue(strategy = GenerationType.AUTO)
	private int id;

	@Column(nullable=false)
	private String name;
	@Column(nullable=false)
	private String info;

	public ReplyTask() {
	}

	public ReplyTask(String name, String info) {
		this.name = name;
		this.info = info;
	}

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getInfo() {
		return info;
	}

	public void setInfo(String info) {
		this.info = info;
	}
}
