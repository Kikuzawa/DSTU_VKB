module org.example.laboratory__3 {
    requires javafx.controls;
    requires javafx.fxml;
    requires javafx.swing;


    opens org.example.laboratory__3 to javafx.fxml;
    exports org.example.laboratory__3;
}