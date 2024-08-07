import os
import cv2
import glob
import time
import pandas as pd
from ultralytics import YOLO
from pathlib import Path

def create_mask(image, reference_image):
    if reference_image.shape[:2] != image.shape[:2]:
        raise ValueError("Les dimensions de l'image de référence et de l'image à traiter ne correspondent pas.")
    mask = cv2.multiply(image, reference_image, scale=1/255.0)
    return mask

def predict_and_draw_boxes(model, image, output_path):
    results = model(image)
    class_counts = {}
    
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf.item()
            cls = int(box.cls.item())
            class_name = model.names[cls]

            if class_name in class_counts:
                class_counts[class_name] += 1
            else:
                class_counts[class_name] = 1

            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f"{class_name} {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imwrite(output_path, image)
    print(f"Image avec boîtes de délimitation enregistrée avec succès : {output_path}")

    return class_counts

def main():
    # folder_path = 'C:/Users/antoi/Documents/AI_Project/Recup_images/Images_Lyon'
    # output_folder = 'C:/Users/antoi/Documents/AI_Project/dashboard_analysis/predict_images'
    # mask_reference_path = 'mask.jpg'  # Chemin vers l'image de référence pour les masques
    # mask_output_folder = 'C:/Users/aerisay/Documents/AI_Project/Recup_images_labellisées/yolo/predict_images_mask'  # Dossier de sortie pour les masques
    # csv_output_path = 'C:/Users/antoi/Documents/AI_Project/dashboard_analysis/detected_classes.csv'  # Chemin vers le fichier CSV de sortie


    folder_path = 'Images_Lyon'
    output_folder = 'predict_images'
    mask_reference_path = 'mask.jpg'  # Chemin vers l'image de référence pour les masques
    # mask_output_folder = 'C:/Users/aerisay/Documents/AI_Project/Recup_images_labellisées/yolo/predict_images_mask'  # Dossier de sortie pour les masques
    csv_output_path = 'detected_classes.csv'  # Chemin vers le fichier CSV de sortie

    # Vérifiez le chemin absolu de l'image de référence
    abs_mask_reference_path = os.path.abspath(mask_reference_path)
    # print(f"Chemin absolu de l'image de référence : {abs_mask_reference_path}")

    # Vérifiez si le fichier existe et est lisible
    if not os.path.exists(mask_reference_path):
        print(f"Erreur: Le fichier {mask_reference_path} n'existe pas.")
        return

    model = YOLO('yolov8m.pt')
    model = YOLO("best.pt")

    reference_image = cv2.imread(mask_reference_path, cv2.IMREAD_COLOR)
    if reference_image is None:
        print(f"Erreur: Impossible de charger l'image de référence à partir de {mask_reference_path}. Vérifiez le chemin d'accès.")
        return

    os.makedirs(output_folder, exist_ok=True)

    processed_images = set()

    while True:
        image_paths = glob.glob(os.path.join(folder_path, '*.jpg'))
        new_images = [img for img in image_paths if img not in processed_images]

        if new_images:
            csv_data = []

            for image_path in new_images:
                image = cv2.imread(image_path, cv2.IMREAD_COLOR)
                if image is None:
                    print(f"Erreur: Impossible de charger l'image à partir de {image_path}.")
                    continue

                try:
                    mask = create_mask(image, reference_image)
                    mask_filename = os.path.basename(image_path)
                    output_path = os.path.join(output_folder, mask_filename)
                    class_counts = predict_and_draw_boxes(model, mask, output_path)

                    for class_name, count in class_counts.items():
                        csv_data.append({
                            'id': mask_filename,
                            'class_name': class_name,
                            'count': count
                        })

                    processed_images.add(image_path)

                except ValueError as e:
                    print(f"Erreur pour l'image {image_path}: {e}")

            if csv_data:
                df = pd.DataFrame(csv_data)
                if os.path.exists(csv_output_path):
                    df.to_csv(csv_output_path, mode='a', header=False, index=False)
                else:
                    df.to_csv(csv_output_path, index=False)
                print(f"Fichier CSV mis à jour avec succès : {csv_output_path}")

        time.sleep(20)

if __name__ == "__main__":
    main()