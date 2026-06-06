from app.logic import (
    PERSON_WARNING,
    SAFE_STATUS,
    TRAFFIC_CONTROL_WARNING,
    VEHICLE_WARNING,
    generate_warnings,
)


def pred(class_name: str, confidence: float = 0.9, center_x: float = 320, center_y: float = 380) -> dict:
    return {
        "class_name": class_name,
        "class_id": 0,
        "confidence": confidence,
        "xyxy": [300, 340, 360, 420],
        "area": 4800,
        "center_x": center_x,
        "center_y": center_y,
    }


def test_person_warning() -> None:
    warnings = generate_warnings(
        [pred("person")],
        conf_threshold=0.35,
        image_shape=(480, 640, 3),
        segmentation_enabled=False,
    )
    assert PERSON_WARNING in warnings


def test_vehicle_warning() -> None:
    warnings = generate_warnings(
        [pred("car", center_x=330, center_y=390)],
        conf_threshold=0.35,
        image_shape=(480, 640, 3),
        segmentation_enabled=False,
    )
    assert VEHICLE_WARNING in warnings


def test_traffic_sign_warning() -> None:
    warnings = generate_warnings(
        [pred("traffic sign", center_x=120, center_y=120)],
        conf_threshold=0.35,
        image_shape=(480, 640, 3),
        segmentation_enabled=False,
    )
    assert TRAFFIC_CONTROL_WARNING in warnings
    assert TRAFFIC_CONTROL_WARNING == "Thông tin: phát hiện biển báo hoặc đèn giao thông"


def test_safe_state() -> None:
    warnings = generate_warnings(
        [],
        conf_threshold=0.35,
        image_shape=(480, 640, 3),
        segmentation_enabled=True,
        road_area_ratio=0.2,
        mask_available=True,
    )
    assert warnings == [SAFE_STATUS]


def test_vietnamese_literals_are_not_mojibake() -> None:
    for text in [PERSON_WARNING, VEHICLE_WARNING, TRAFFIC_CONTROL_WARNING, SAFE_STATUS]:
        assert "Ã" not in text
        assert "áº" not in text
        assert "á»" not in text
