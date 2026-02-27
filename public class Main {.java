public class Main {
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.regex.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

// employee class to represent employee data

class Employee {
    int    id;
    String username;
    String passwordHash;
    String firstName;
    String lastName;
    String email;
    String role;         // "admin", "manager", "employee"
    boolean isActive;

    public Employee(int id, String username, String passwordHash,
                    String firstName, String lastName,
                    String email, String role, boolean isActive) {
        this.id           = id;
        this.username     = username;
        this.passwordHash = passwordHash;
        this.firstName    = firstName;
        this.lastName     = lastName;
        this.email        = email;
        this.role         = role;
        this.isActive     = isActive;
    }

    @Override
    public String toString() {
        return String.format("ID: %d | Name: %s %s | Username: %s | Role: %s | Active: %b",
                id, firstName, lastName, username, role, isActive);
    }
}

// ─────────────────────────────────────────────
//  EmployeePortalHelper — all backend methods
// ─────────────────────────────────────────────

public class EmployeePortalHelper {



    public static String hashPassword(String password) {
        long hashValue = 0;
        for (char c : password.toCharArray()) {
            hashValue = hashValue * 31 + c;
        }
        return Long.toHexString(hashValue);
    }
}
}