package com.song.dao.mysqlimpl;

import com.song.model.mysqlmodel.User;

import java.util.List;

public interface IUserDao {

	public abstract List<User> getAllUsers();

	public abstract User getUserByID(int userId);

	public abstract String insertUser(User user);

	public abstract String updateUser(int userId, User user);

	public abstract String deleteUser(int userId);
}