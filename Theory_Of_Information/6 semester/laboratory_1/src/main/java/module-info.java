module com.kikuzawa.laboratory_1 {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.kikuzawa.laboratory_1 to javafx.fxml;
    exports com.kikuzawa.laboratory_1;
}