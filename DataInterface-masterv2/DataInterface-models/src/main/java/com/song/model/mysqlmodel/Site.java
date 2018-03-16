package com.song.model.mysqlmodel;

import javax.persistence.*;
import java.io.Serializable;

@Entity
@Table(name="site")
public class Site implements Serializable {

	@Id
	@GeneratedValue(strategy = GenerationType.AUTO)
	private int site_id;

	@Column(nullable=false)
	private String site_url;

	@Column(nullable=false)
	private String site_name;

	@Column(nullable=false)
	private int site_type;

	@Column(nullable=false)
	private String site_sign;

	@Column(nullable=false)
	private String post_url;

	@Column(nullable=false)
	private String region;

	@Column(nullable=false)
	private int weight;

	@Column(nullable=false)
	private int mianpage_count;

	public Site() {
	}

	public Site(String site_url, String site_name, int site_type, String site_sign, String post_url, String region, int weight, int mianpage_count) {
		this.site_url = site_url;
		this.site_name = site_name;
		this.site_type = site_type;
		this.site_sign = site_sign;
		this.post_url = post_url;
		this.region = region;
		this.weight = weight;
		this.mianpage_count = mianpage_count;
	}

	public int getSite_id() {
		return site_id;
	}

	public void setSite_id(int site_id) {
		this.site_id = site_id;
	}

	public String getSite_url() {
		return site_url;
	}

	public void setSite_url(String site_url) {
		this.site_url = site_url;
	}

	public String getSite_name() {
		return site_name;
	}

	public void setSite_name(String site_name) {
		this.site_name = site_name;
	}

	public int getSite_type() {
		return site_type;
	}

	public void setSite_type(int site_type) {
		this.site_type = site_type;
	}

	public String getSite_sign() {
		return site_sign;
	}

	public void setSite_sign(String site_sign) {
		this.site_sign = site_sign;
	}

	public String getPost_url() {
		return post_url;
	}

	public void setPost_url(String post_url) {
		this.post_url = post_url;
	}

	public String getRegion() {
		return region;
	}

	public void setRegion(String region) {
		this.region = region;
	}

	public int getWeight() {
		return weight;
	}

	public void setWeight(int weight) {
		this.weight = weight;
	}

	public int getMianpage_count() {
		return mianpage_count;
	}

	public void setMianpage_count(int mianpage_count) {
		this.mianpage_count = mianpage_count;
	}
}
