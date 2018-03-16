package com.song.api.mysqlservice;

import com.song.api.mysqlimpl.IUserService;
import com.song.dao.mysqlimpl.IUserDao;
import com.song.model.mysqlmodel.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;


@Service
public class UserServiceImpl implements IUserService {

    @Autowired
    private IUserDao userDaoImpl;

    @Override
    public List<User> getAllUsers() {
        return userDaoImpl.getAllUsers();
    }

    @Override
    public User getUserByID(int id) {
        return userDaoImpl.getUserByID(id);
    }

    @Override
    public String insertUser(User user) {
        return userDaoImpl.insertUser(user);
    }

    @Override
    public String updateUser(int userId, User user) {
        return userDaoImpl.updateUser(userId, user);
    }

    @Override
    public String deleteUser(int userId) {
        return userDaoImpl.deleteUser(userId);
    }

}