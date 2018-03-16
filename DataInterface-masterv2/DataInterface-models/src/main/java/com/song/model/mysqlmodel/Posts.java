package com.song.model.mysqlmodel;

import org.hibernate.annotations.Type;

import javax.persistence.*;
import java.io.Serializable;
import java.util.Date;

@Entity
@Table(name="posts")
public class Posts implements Serializable {

	private String urlmd5;
	@Id

	private String url;
	private String tid;
	private String title;
	private Integer site_id;
	@Type(type = "text")
	private String content;
	private String author;
	private Date post_time;
	private Integer read_count;
	private Integer reply_count;
	private Integer screen_print;

	public String getUrlmd5() {
		return urlmd5;
	}

	public void setUrlmd5(String urlmd5) {
		this.urlmd5 = urlmd5;
	}

	public String getUrl() {
		return url;
	}

	public void setUrl(String url) {
		this.url = url;
	}

	public String getTid() {
		return tid;
	}

	public void setTid(String tid) {
		this.tid = tid;
	}

	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public Integer getSite_id() {
		return site_id;
	}

	public void setSite_id(Integer site_id) {
		this.site_id = site_id;
	}

	public String getContent() {
		return content;
	}

	public void setContent(String content) {
		this.content = content;
	}

	public String getAuthor() {
		return author;
	}

	public void setAuthor(String author) {
		this.author = author;
	}

	public Date getPost_time() {
		return post_time;
	}

	public void setPost_time(Date post_time) {
		this.post_time = post_time;
	}

	public Integer getRead_count() {
		return read_count;
	}

	public void setRead_count(Integer read_count) {
		this.read_count = read_count;
	}

	public Integer getReply_count() {
		return reply_count;
	}

	public void setReply_count(Integer reply_count) {
		this.reply_count = reply_count;
	}

	public Integer getScreen_print() {
		return screen_print;
	}

	public void setScreen_print(Integer screen_print) {
		this.screen_print = screen_print;
	}
}
