module com.kikuzawa.laboratory_2 {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.kikuzawa.laboratory_2 to javafx.fxml;
    exports com.kikuzawa.laboratory_2;
}