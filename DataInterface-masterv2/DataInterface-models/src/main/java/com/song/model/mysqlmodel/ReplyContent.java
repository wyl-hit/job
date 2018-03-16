package com.song.model.mysqlmodel;

import javax.persistence.*;
import java.io.Serializable;

@Entity
@Table(name="Reply_content")
public class ReplyContent implements Serializable {

	@Id
	@GeneratedValue(strategy = GenerationType.AUTO)
	private int id;

	@Column(nullable=false)
	private int task_id;
	@Column(nullable=false)
	private String content;

	public ReplyContent() {
	}

	public ReplyContent(int task_id, String content) {
		this.task_id = task_id;
		this.content = content;
	}

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public int getTask_id() {
		return task_id;
	}

	public void setTask_id(int task_id) {
		this.task_id = task_id;
	}

	public String getContent() {
		return content;
	}

	public void setContent(String content) {
		this.content = content;
	}
}
