from controllers.admin_controller import add_admin

# Add admin with username "admin" and password "admin"
admin_id = add_admin(
    username="admin",
    password="admin",
    first_name="System",
    last_name="Administrator"
)

if admin_id:
    print(f"Admin created successfully with ID: {admin_id}")
else:
    print("Failed to create admin")