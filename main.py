import os
import tkinter as tk
from tkinter import messagebox, ttk

from database.create_database import create_db
from database.db import Database
from repositories.course_repository import CourseRepository
from repositories.schedule_repository import ScheduleRepository
from services.auth_service import AuthService
from services.course_service import CourseService
from services.enrollment_service import EnrollmentService


APP_TITLE = "Hệ thống đăng ký học phần - Nhóm 8"
APP_SIZE = "1120x720"
APP_MIN_SIZE = (980, 620)

LOGIN_DEFAULTS = {
    "username": "",
    "password": "",
}

MESSAGES = {
    "Invalid username or password": "Tên đăng nhập hoặc mật khẩu không đúng.",
    "Account is inactive": "Tài khoản đang bị khóa.",
    "Username and email are required": "Vui lòng nhập tên đăng nhập và email.",
    "Username or email does not exist": "Tên đăng nhập hoặc email không tồn tại.",
    "New password and confirmation are required": "Vui lòng nhập mật khẩu mới và xác nhận mật khẩu.",
    "Passwords do not match": "Mật khẩu xác nhận không khớp.",
    "New password must be at least 6 characters": "Mật khẩu mới phải có ít nhất 6 ký tự.",
    "User not found": "Không tìm thấy người dùng.",
    "You are already enrolled in this class": "Bạn đã đăng ký lớp học phần này.",
    "Class not found": "Không tìm thấy lớp học phần.",
    "This class is full": "Lớp học phần đã đủ số lượng.",
    "Prerequisite not met": "Chưa đạt môn tiên quyết.",
    "Schedule conflict detected": "Lịch học bị trùng.",
    "Enrollment not found": "Không tìm thấy đăng ký học phần.",
    "Course name is required": "Vui lòng nhập tên môn học.",
    "Credits must be greater than 0": "Số tín chỉ phải lớn hơn 0.",
    "Fee must be a non-negative number": "Học phí không được âm.",
    "Course name already exists": "Tên môn học đã tồn tại.",
    "Course not found": "Không tìm thấy môn học.",
    "Instructor name is required": "Vui lòng nhập tên giảng viên.",
    "Max enrollment must be greater than 0": "Sĩ số tối đa phải lớn hơn 0.",
}

VI_TEXT = {
    "Student": "Sinh viên",
    "Admin": "Quản trị viên",
    "Active": "Hoạt động",
    "Inactive": "Khóa",
    "Open": "Đang mở",
    "Pass": "Đạt",
    "Fail": "Không đạt",
    "Male": "Nam",
    "Female": "Nữ",
    "Introduction to Programming": "Nhập môn lập trình",
    "Data Structures and Algorithms": "Cấu trúc dữ liệu và giải thuật",
    "Database Systems": "Hệ cơ sở dữ liệu",
    "Operating Systems": "Hệ điều hành",
    "Computer Networks": "Mạng máy tính",
    "Software Engineering": "Công nghệ phần mềm",
}

STUDENT_CLASS_COLUMNS = (
    "Mã lớp", "Môn học", "Tín chỉ", "Giảng viên",
    "Đã đăng ký", "Tối đa", "Lịch học", "Môn tiên quyết"
)
ENROLLMENT_COLUMNS = (
    "Mã đăng ký", "Mã lớp", "Môn học", "Giảng viên", "Ngày đăng ký"
)
SCHEDULE_COLUMNS = (
    "Mã lớp", "Thời gian", "Ngày bắt đầu", "Ngày kết thúc", "Phòng"
)
RESULT_COLUMNS = ("Môn học", "Điểm GPA", "Trạng thái")
ADMIN_COURSE_COLUMNS = (
    "Mã môn", "Tên môn", "Tín chỉ", "Học kỳ", "Trạng thái", "Học phí", "Môn tiên quyết"
)
ADMIN_CLASS_COLUMNS = (
    "Mã lớp", "Môn học", "Giảng viên", "Đã đăng ký", "Tối đa", "Trạng thái"
)
USER_COLUMNS = (
    "Mã người dùng", "Tên đăng nhập", "Vai trò", "Giới tính", "Trạng thái"
)


def text_vi(value):
    return VI_TEXT.get(value, value)


def error_vi(error):
    message = str(error)
    prefix = "Prerequisite not met: "
    if message.startswith(prefix):
        missing = [
            text_vi(course_name.strip())
            for course_name in message[len(prefix):].split(",")
            if course_name.strip()
        ]
        return "Chưa đạt môn tiên quyết: " + ", ".join(missing)
    return MESSAGES.get(message, message)


class CourseRegistrationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_SIZE)
        self.minsize(*APP_MIN_SIZE)

        self.auth_service = AuthService()
        self.course_service = CourseService()
        self.enrollment_service = EnrollmentService()
        self.course_repo = CourseRepository()
        self.schedule_repo = ScheduleRepository()
        self.db = Database()

        self.current_user = None
        self.current_student = None
        self.selected_class_id = None
        self.selected_enrollment_id = None

        self._setup_style()
        self._show_login()

    # ---------- Layout helpers ----------
    def _setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#eef8f0")
        style.configure("Card.TFrame", background="#ffffff", relief="flat")
        style.configure("TLabel", background="#eef8f0", foreground="#173b25")
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("Subtitle.TLabel", foreground="#4f6f59")
        style.configure("TButton", padding=(12, 7), font=("Segoe UI", 10, "bold"))
        style.map("TButton", background=[("active", "#1f7a3a")])
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def _clear_window(self):
        for child in self.winfo_children():
            child.destroy()

    def _make_tree(self, parent, columns):
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)
        tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, width=self._column_width(column), minwidth=100, anchor="w", stretch=False)
        return tree

    def _column_width(self, column):
        widths = {
            "Mã đăng ký": 120,
            "Mã người dùng": 130,
            "Tên đăng nhập": 150,
            "Môn học": 240,
            "Môn tiên quyết": 260,
            "Giảng viên": 190,
            "Lịch học": 260,
            "Thời gian": 260,
            "Ngày bắt đầu": 140,
            "Ngày kết thúc": 140,
            "Trạng thái": 130,
            "Sĩ số tối đa": 130,
        }
        return widths.get(column, 120)

    def _set_tree_rows(self, tree, rows):
        tree.delete(*tree.get_children())
        for row in rows:
            tree.insert("", "end", values=row)

    def _add_form_field(self, parent, label, variable, pair_index):
        label_col = pair_index * 2
        input_col = label_col + 1
        ttk.Label(parent, text=label).grid(row=0, column=label_col, padx=(0, 5), sticky="w")
        ttk.Entry(parent, textvariable=variable, width=18).grid(
            row=0, column=input_col, padx=(0, 12), sticky="ew"
        )

    # ---------- Login ----------
    def _show_login(self):
        self._clear_window()
        self.current_user = None
        self.current_student = None

        wrapper = tk.Frame(self, bg="#dff3e4")
        wrapper.pack(fill="both", expand=True)

        card = ttk.Frame(wrapper, padding=32, style="Card.TFrame")
        card.place(relx=0.5, rely=0.5, anchor="center", width=420)

        self.username_var = tk.StringVar(value=LOGIN_DEFAULTS["username"])
        self.password_var = tk.StringVar(value=LOGIN_DEFAULTS["password"])

        ttk.Label(
            card, text="Đăng ký học phần UTH",
            style="Title.TLabel", background="#ffffff"
        ).pack(anchor="w")
        ttk.Label(
            card,
            text="Nhập tài khoản sinh viên để bắt đầu đăng ký học phần.",
            style="Subtitle.TLabel",
            background="#ffffff",
        ).pack(anchor="w", pady=(4, 24))

        self._add_login_entry(card, "Tên đăng nhập", self.username_var)
        self._add_login_entry(card, "Mật khẩu", self.password_var, show="*")

        ttk.Button(card, text="Đăng nhập", command=self._login).pack(fill="x")
        ttk.Button(card, text="Quên mật khẩu?", command=self._show_forgot_password).pack(
            fill="x", pady=(10, 0)
        )

    def _add_login_entry(self, parent, label, variable, show=None):
        ttk.Label(parent, text=label, background="#ffffff").pack(anchor="w")
        ttk.Entry(parent, textvariable=variable, show=show).pack(fill="x", pady=(4, 14))

    def _login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        if not username or not password:
            messagebox.showwarning(
                "Thiếu thông tin",
                "Vui lòng nhập tên đăng nhập và mật khẩu.",
            )
            return

        try:
            self.current_user = self.auth_service.login(username, password)
            self.current_student = self._find_student_by_user(self.current_user.userID)
            self._show_main_screen()
        except Exception as exc:
            messagebox.showerror("Đăng nhập thất bại", error_vi(exc))

    def _show_forgot_password(self):
        self._clear_window()

        wrapper = tk.Frame(self, bg="#dff3e4")
        wrapper.pack(fill="both", expand=True)

        card = ttk.Frame(wrapper, padding=32, style="Card.TFrame")
        card.place(relx=0.5, rely=0.5, anchor="center", width=440)

        self.forgot_username_var = tk.StringVar()
        self.forgot_email_var = tk.StringVar()

        ttk.Label(
            card, text="Xác minh danh tính",
            style="Title.TLabel", background="#ffffff"
        ).pack(anchor="w")
        ttk.Label(
            card,
            text="Nhập tên đăng nhập và email đã đăng ký để xác minh tài khoản.",
            style="Subtitle.TLabel",
            background="#ffffff",
        ).pack(anchor="w", pady=(4, 24))

        self._add_login_entry(card, "Tên đăng nhập", self.forgot_username_var)
        self._add_login_entry(card, "Email đã đăng ký", self.forgot_email_var)

        ttk.Button(card, text="Xác minh", command=self._verify_reset_identity).pack(fill="x")
        ttk.Button(card, text="Quay lại đăng nhập", command=self._show_login).pack(
            fill="x", pady=(10, 0)
        )

    def _verify_reset_identity(self):
        username = self.forgot_username_var.get().strip()
        email = self.forgot_email_var.get().strip()
        if not username or not email:
            messagebox.showwarning(
                "Thiếu thông tin",
                "Vui lòng nhập tên đăng nhập và email.",
            )
            return

        try:
            user = self.auth_service.verify_identity(username, email)
            messagebox.showinfo(
                "Xác minh thành công",
                "Thông tin tài khoản hợp lệ. Vui lòng đặt lại mật khẩu.",
            )
            self._show_reset_password(user)
        except Exception as exc:
            messagebox.showerror("Không thể xác minh", error_vi(exc))

    def _show_reset_password(self, user):
        self._clear_window()

        wrapper = tk.Frame(self, bg="#dff3e4")
        wrapper.pack(fill="both", expand=True)

        card = ttk.Frame(wrapper, padding=32, style="Card.TFrame")
        card.place(relx=0.5, rely=0.5, anchor="center", width=440)

        self.reset_user = user
        self.new_password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()

        ttk.Label(
            card, text="Đặt lại mật khẩu",
            style="Title.TLabel", background="#ffffff"
        ).pack(anchor="w")
        ttk.Label(
            card,
            text=f"Tài khoản đã xác minh: {user.userName}",
            style="Subtitle.TLabel",
            background="#ffffff",
        ).pack(anchor="w", pady=(4, 24))

        self._add_login_entry(card, "Mật khẩu mới", self.new_password_var, show="*")
        self._add_login_entry(card, "Xác nhận mật khẩu", self.confirm_password_var, show="*")

        ttk.Button(card, text="Cập nhật mật khẩu", command=self._reset_password).pack(fill="x")
        ttk.Button(card, text="Quay lại xác minh", command=self._show_forgot_password).pack(
            fill="x", pady=(10, 0)
        )

    def _reset_password(self):
        new_password = self.new_password_var.get()
        confirm_password = self.confirm_password_var.get()
        if not new_password or not confirm_password:
            messagebox.showwarning(
                "Thiếu thông tin",
                "Vui lòng nhập mật khẩu mới và xác nhận mật khẩu.",
            )
            return
        if new_password != confirm_password:
            messagebox.showerror(
                "Mật khẩu không khớp",
                "Mật khẩu xác nhận không khớp.",
            )
            return
        if len(new_password) < 6:
            messagebox.showwarning(
                "Mật khẩu chưa hợp lệ",
                "Mật khẩu mới phải có ít nhất 6 ký tự.",
            )
            return

        try:
            self.auth_service.reset_password(
                self.reset_user.userID,
                new_password,
                confirm_password,
            )
            messagebox.showinfo(
                "Thành công",
                "Mật khẩu đã được cập nhật. Vui lòng đăng nhập bằng mật khẩu mới.",
            )
            self._show_login()
        except Exception as exc:
            messagebox.showerror("Không thể đặt lại mật khẩu", error_vi(exc))

    def _find_student_by_user(self, user_id):
        return self.db.fetch_one("SELECT * FROM Student WHERE userID = ?", (user_id,))

    # ---------- Main shell ----------
    def _show_main_screen(self):
        self._clear_window()

        root = ttk.Frame(self)
        root.pack(fill="both", expand=True)

        self._build_sidebar(root)
        main = ttk.Frame(root, padding=20)
        main.pack(side="left", fill="both", expand=True)

        title = self.current_user.userName
        if self.current_student:
            title = self.current_student["studentName"]

        ttk.Label(main, text=f"Xin chào, {title}", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            main,
            text="Chương trình đăng ký học phần theo mô hình hướng đối tượng.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(2, 16))

        tabs = ttk.Notebook(main)
        tabs.pack(fill="both", expand=True)

        if self.current_user.role == "Student":
            self._build_student_tabs(tabs)
        else:
            self._build_admin_tabs(tabs)

    def _build_sidebar(self, parent):
        sidebar = tk.Frame(parent, width=220, bg="#14532d")
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar, text="NHÓM 8", bg="#14532d", fg="#ffffff",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", padx=22, pady=(24, 4))
        tk.Label(
            sidebar, text=text_vi(self.current_user.role),
            bg="#14532d", fg="#bbf7d0", font=("Segoe UI", 10)
        ).pack(anchor="w", padx=22, pady=(0, 22))

        ttk.Button(sidebar, text="Đăng xuất", command=self._show_login).pack(
            side="bottom", fill="x", padx=18, pady=20
        )

    # ---------- Student screen ----------
    def _build_student_tabs(self, tabs):
        register_tab = ttk.Frame(tabs, padding=12)
        enrollment_tab = ttk.Frame(tabs, padding=12)
        schedule_tab = ttk.Frame(tabs, padding=12)
        result_tab = ttk.Frame(tabs, padding=12)

        tabs.add(register_tab, text="Đăng ký học phần")
        tabs.add(enrollment_tab, text="Lớp đã đăng ký")
        tabs.add(schedule_tab, text="Thời khóa biểu")
        tabs.add(result_tab, text="Kết quả học tập")

        self.class_tree = self._make_tree(register_tab, STUDENT_CLASS_COLUMNS)
        self.class_tree.bind("<<TreeviewSelect>>", self._select_class)
        ttk.Button(
            register_tab,
            text="Đăng ký lớp đã chọn",
            command=self._enroll_selected_class,
        ).pack(anchor="e", pady=12)

        self.enrollment_tree = self._make_tree(enrollment_tab, ENROLLMENT_COLUMNS)
        self.enrollment_tree.bind("<<TreeviewSelect>>", self._select_enrollment)
        ttk.Button(
            enrollment_tab,
            text="Hủy đăng ký đã chọn",
            command=self._cancel_selected_enrollment,
        ).pack(anchor="e", pady=12)

        self.schedule_tree = self._make_tree(schedule_tab, SCHEDULE_COLUMNS)

        self.result_tree = self._make_tree(result_tab, RESULT_COLUMNS)

        self._refresh_student_data()

    def _refresh_student_data(self):
        student_id = self.current_student["studentID"]
        self._set_tree_rows(self.class_tree, self._get_class_rows())
        self._set_tree_rows(self.enrollment_tree, self._get_enrollment_rows(student_id))
        self._set_tree_rows(self.schedule_tree, self._get_schedule_rows(student_id))
        self._set_tree_rows(self.result_tree, self._get_result_rows(student_id))

    def _select_class(self, _event):
        values = self.class_tree.item(self.class_tree.focus(), "values")
        self.selected_class_id = int(values[0]) if values else None

    def _select_enrollment(self, _event):
        values = self.enrollment_tree.item(self.enrollment_tree.focus(), "values")
        self.selected_enrollment_id = int(values[0]) if values else None

    def _enroll_selected_class(self):
        if not self.selected_class_id:
            messagebox.showwarning("Chưa chọn dữ liệu", "Vui lòng chọn một lớp học phần trước.")
            return

        try:
            student_id = self.current_student["studentID"]
            self.enrollment_service.enroll_course(student_id, self.selected_class_id)
            self._refresh_student_data()
            messagebox.showinfo("Thành công", "Đăng ký học phần thành công.")
        except Exception as exc:
            messagebox.showerror("Không thể đăng ký", error_vi(exc))

    def _cancel_selected_enrollment(self):
        if not self.selected_enrollment_id:
            messagebox.showwarning("Chưa chọn dữ liệu", "Vui lòng chọn một đăng ký học phần trước.")
            return

        try:
            self.enrollment_service.cancel_enrollment(self.selected_enrollment_id)
            self.selected_enrollment_id = None
            self._refresh_student_data()
            messagebox.showinfo("Thành công", "Hủy đăng ký học phần thành công.")
        except Exception as exc:
            messagebox.showerror("Không thể hủy đăng ký", error_vi(exc))

    # ---------- Admin screen ----------
    def _build_admin_tabs(self, tabs):
        courses_tab = ttk.Frame(tabs, padding=12)
        classes_tab = ttk.Frame(tabs, padding=12)
        users_tab = ttk.Frame(tabs, padding=12)

        tabs.add(courses_tab, text="Môn học")
        tabs.add(classes_tab, text="Lớp học phần")
        tabs.add(users_tab, text="Người dùng")

        self._build_course_form(courses_tab)
        self.admin_course_tree = self._make_tree(courses_tab, ADMIN_COURSE_COLUMNS)

        self._build_class_form(classes_tab)
        self.admin_class_tree = self._make_tree(classes_tab, ADMIN_CLASS_COLUMNS)

        self.user_tree = self._make_tree(users_tab, USER_COLUMNS)

        self._refresh_admin_data()

    def _build_course_form(self, parent):
        form = ttk.Frame(parent)
        form.pack(fill="x", pady=(0, 12))

        self.new_course_name = tk.StringVar()
        self.new_course_credit = tk.StringVar(value="3")
        self.new_course_semester = tk.StringVar(value="1")
        self.new_course_fee = tk.StringVar(value="4500000")

        self._add_form_field(form, "Tên môn", self.new_course_name, 0)
        self._add_form_field(form, "Tín chỉ", self.new_course_credit, 1)
        self._add_form_field(form, "Học kỳ", self.new_course_semester, 2)
        self._add_form_field(form, "Học phí", self.new_course_fee, 3)
        ttk.Button(form, text="Thêm môn", command=self._add_course).grid(
            row=0, column=8, padx=8, sticky="ew"
        )

    def _build_class_form(self, parent):
        form = ttk.Frame(parent)
        form.pack(fill="x", pady=(0, 12))

        self.new_class_course = tk.StringVar(value="1")
        self.new_class_teacher = tk.StringVar()
        self.new_class_max = tk.StringVar(value="40")

        self._add_form_field(form, "Mã môn", self.new_class_course, 0)
        self._add_form_field(form, "Giảng viên", self.new_class_teacher, 1)
        self._add_form_field(form, "Sĩ số tối đa", self.new_class_max, 2)
        ttk.Button(form, text="Tạo lớp", command=self._create_class).grid(
            row=0, column=6, padx=8, sticky="ew"
        )

    def _refresh_admin_data(self):
        self._set_tree_rows(self.admin_course_tree, self._get_course_rows())
        self._set_tree_rows(self.admin_class_tree, self._get_admin_class_rows())
        self._set_tree_rows(self.user_tree, self._get_user_rows())

    def _add_course(self):
        try:
            self.course_service.add_course(
                self.new_course_name.get(),
                int(self.new_course_credit.get()),
                float(self.new_course_fee.get()),
                self.new_course_semester.get(),
            )
            self.new_course_name.set("")
            self._refresh_admin_data()
            messagebox.showinfo("Thành công", "Thêm môn học thành công.")
        except Exception as exc:
            messagebox.showerror("Không thể thêm môn học", error_vi(exc))

    def _create_class(self):
        try:
            self.course_service.create_class(
                int(self.new_class_course.get()),
                self.new_class_teacher.get(),
                int(self.new_class_max.get()),
            )
            self.new_class_teacher.set("")
            self._refresh_admin_data()
            messagebox.showinfo("Thành công", "Tạo lớp học phần thành công.")
        except Exception as exc:
            messagebox.showerror("Không thể tạo lớp", error_vi(exc))

    # ---------- Data queries ----------
    def _format_prerequisites(self, prerequisites):
        if not prerequisites:
            return "Không có"
        names = []
        for prerequisite in prerequisites:
            name = getattr(prerequisite, "courseName", None)
            names.append(text_vi(name) if name else str(prerequisite.courseID))
        return ", ".join(names)

    def _format_prerequisite_names(self, names):
        if not names:
            return "Không có"
        return ", ".join(text_vi(name.strip()) for name in names.split(",") if name.strip())

    def _get_class_rows(self):
        rows = self.db.fetch_all(
            """SELECT cc.courseClassID, c.courseName, c.credit, t.teacherName,
                      cc.currentEnroll, cc.maxEnroll,
                      COALESCE(s.session, 'Chưa xếp lịch') AS session,
                      GROUP_CONCAT(pc.courseName, ',') AS prerequisites,
                      cc.status
               FROM coursesClass cc
               JOIN Courses c ON c.courseID = cc.courseID
               LEFT JOIN hasPrerequisite hp ON hp.courseID = c.courseID
               LEFT JOIN Courses pc ON pc.courseID = hp.prerequisiteID
               LEFT JOIN Teacher t ON t.teacherID = cc.teacherID
               LEFT JOIN Schedule s ON s.courseClassID = cc.courseClassID
               GROUP BY cc.courseClassID, c.courseName, c.credit, t.teacherName,
                        cc.currentEnroll, cc.maxEnroll, s.session, cc.status
               ORDER BY cc.courseClassID"""
        )
        return [
            (
                row["courseClassID"],
                text_vi(row["courseName"]),
                row["credit"],
                row["teacherName"],
                row["currentEnroll"],
                row["maxEnroll"],
                row["session"],
                self._format_prerequisite_names(row["prerequisites"]),
            )
            for row in rows
        ]

    def _get_enrollment_rows(self, student_id):
        rows = self.db.fetch_all(
            """SELECT e.enrollID, e.courseClassID, c.courseName,
                      t.teacherName, e.enrollDate
               FROM Enrollment e
               JOIN coursesClass cc ON cc.courseClassID = e.courseClassID
               JOIN Courses c ON c.courseID = cc.courseID
               LEFT JOIN Teacher t ON t.teacherID = cc.teacherID
               WHERE e.studentID = ?
               ORDER BY e.enrollDate DESC, e.enrollID DESC""",
            (student_id,),
        )
        return [
            (
                row["enrollID"],
                row["courseClassID"],
                text_vi(row["courseName"]),
                row["teacherName"],
                row["enrollDate"],
            )
            for row in rows
        ]

    def _get_schedule_rows(self, student_id):
        schedules = self.schedule_repo.find_by_student(student_id)
        return [
            (
                schedule.courseClassID,
                schedule.time,
                schedule.startDate,
                schedule.endDate,
                schedule.roomCode or "Chưa có",
            )
            for schedule in schedules
        ]

    def _get_result_rows(self, student_id):
        rows = self.db.fetch_all(
            """SELECT c.courseName, r.gpa, r.status
               FROM studentResult r
               JOIN Courses c ON c.courseID = r.courseID
               WHERE r.studentID = ?
               ORDER BY c.courseID""",
            (student_id,),
        )
        return [
            (text_vi(row["courseName"]), row["gpa"], text_vi(row["status"]))
            for row in rows
        ]

    def _get_course_rows(self):
        return [
            (
                course.courseID,
                text_vi(course.courseName),
                course.credit,
                course.semester,
                text_vi(course.status),
                course.fee,
                self._format_prerequisites(course.prerequisites),
            )
            for course in self.course_repo.find_all()
        ]

    def _get_admin_class_rows(self):
        return [
            (row[0], row[1], row[3], row[4], row[5], text_vi("Open"))
            for row in self._get_class_rows()
        ]

    def _get_user_rows(self):
        users = self.db.fetch_all("SELECT * FROM Users ORDER BY userID")
        return [
            (
                user["userID"],
                user["userName"],
                text_vi(user["role"]),
                text_vi(user["sex"]),
                text_vi(user["status"]),
            )
            for user in users
        ]


def ensure_database():
    db_path = os.path.join(os.path.dirname(__file__), "database", "app.db")
    if not os.path.exists(db_path):
        create_db()


def main():
    ensure_database()
    app = CourseRegistrationApp()
    app.mainloop()


if __name__ == "__main__":
    main()
