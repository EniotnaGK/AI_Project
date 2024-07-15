import os
import cv2
import glob
import pandas as pd
from ultralytics import YOLO
from pathlib import Path

def create_mask(image, reference_image):
    # Vérifier si les dimensions de l'image de référence correspondent à celles de l'image à traiter
    if reference_image.shape[:2] != image.shape[:2]:
        raise ValueError("Les dimensions de l'image de référence et de l'image à traiter ne correspondent pas.")
    
    # Créer le masque en multipliant pixel par pixel avec l'image de référence
    mask = cv2.multiply(image, reference_image, scale=1/255.0)
    return mask

def predict_and_draw_boxes(model, image, output_path):
    results = model(image)

    class_counts = {}
    
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Utilisation de box.xyxy pour obtenir les coordonnées
            conf = box.conf.item()
            cls = int(box.cls.item())
            class_name = model.names[cls]

            # Mettre à jour le compteur de classes
            if class_name in class_counts:
                class_counts[class_name] += 1
            else:
                class_counts[class_name] = 1

            # Draw bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # Put label above the bounding box
            cv2.putText(image, f"{class_name} {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Save the image with bounding boxes
    cv2.imwrite(output_path, image)
    print(f"Image avec boîtes de délimitation enregistrée avec succès : {output_path}")

    return class_counts

def main():
    folder_path = 'C:/Users/antoi/Documents/AI_Project/Recup_images/Images_Lyon'
    output_folder = 'C:/Users/antoi/Documents/AI_Project/model/predict_images'
    mask_reference_path = 'mask.jpg'  # Chemin vers l'image de référence pour les masques
    # mask_output_folder = 'C:/Users/aerisay/Documents/AI_Project/Recup_images_labellisées/yolo/predict_images_mask'  # Dossier de sortie pour les masques
    csv_output_path = 'C:/Users/antoi/Documents/AI_Project/Recup_images/detected_classes.csv'  # Chemin vers le fichier CSV de sortie

    model = YOLO('yolov8m.pt')
    model = YOLO("best.pt")  # load a custom model

    # Charger l'image de référence avec OpenCV
    reference_image = cv2.imread(mask_reference_path, cv2.IMREAD_COLOR)
    if reference_image is None:
        print(f"Erreur: Impossible de charger l'image de référence à partir de {mask_reference_path}. Vérifiez le chemin d'accès.")
        return

    # Assurez-vous que les dossiers de sortie existent
    os.makedirs(output_folder, exist_ok=True)
    # os.makedirs(mask_output_folder, exist_ok=True)

    # Récupérer les chemins des images du dossier d'entrée
    image_paths = glob.glob(os.path.join(folder_path, '*.jpg'))

    csv_data = []

    for image_path in image_paths:
        # Charger l'image à traiter
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if image is None:
            print(f"Erreur: Impossible de charger l'image à partir de {image_path}.")
            continue

        try:
            # Créer le masque
            mask = create_mask(image, reference_image)

            # Déterminer le nom du fichier de sortie pour le masque
            mask_filename = os.path.basename(image_path)
            # mask_output_path = os.path.join(mask_output_folder, mask_filename)

            # Enregistrer le masque dans le dossier de sortie
            # cv2.imwrite(mask_output_path, mask)
            # print(f"Masque créé et enregistré avec succès : {mask_output_path}")

            # Effectuer la prédiction et dessiner les boîtes de délimitation
            output_path = os.path.join(output_folder, mask_filename)
            class_counts = predict_and_draw_boxes(model, mask, output_path)

            # Ajouter les résultats au CSV
            for class_name, count in class_counts.items():
                csv_data.append({
                    'id': mask_filename,
                    'class_name': class_name,
                    'count': count
                })

        except ValueError as e:
            print(f"Erreur pour l'image {image_path}: {e}")

    # Enregistrer les résultats dans un fichier CSV
    df = pd.DataFrame(csv_data)
    df.to_csv(csv_output_path, index=False)
    print(f"Fichier CSV enregistré avec succès : {csv_output_path}")

if __name__ == "__main__":
    main()


#     import os
# import cv2
# import glob
# import torch
# import pandas as pd
# from ultralytics import YOLO
# from pathlib import Path

# def create_mask(image, reference_image):
#     # Vérifier si les dimensions de l'image de référence correspondent à celles de l'image à traiter
#     if reference_image.shape[:2] != image.shape[:2]:
#         raise ValueError("Les dimensions de l'image de référence et de l'image à traiter ne correspondent pas.")
    
#     # Créer le masque en multipliant pixel par pixel avec l'image de référence
#     mask = cv2.multiply(image, reference_image, scale=1/255.0)
#     return mask

# def predict_and_draw_boxes(model, image, output_path):
#     results = model(image)

#     class_list = []
    
#     for result in results:
#         for box in result.boxes:
#             x1, y1, x2, y2 = map(int, box.xyxy[0])  # Utilisation de box.xyxy pour obtenir les coordonnées
#             conf = box.conf.item()
#             cls = int(box.cls.item())
#             label = f"{model.names[cls]} {conf:.2f}"
            
#             # Ajouter la classe détectée à la liste
#             class_list.append(model.names[cls])

#             # Draw bounding box
#             cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             # Put label above the bounding box
#             cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#     # Save the image with bounding boxes
#     cv2.imwrite(output_path, image)
#     print(f"Image avec boîtes de délimitation enregistrée avec succès : {output_path}")

#     return class_list

# def main():
#     folder_path = 'C:/Users/aerisay/Documents/AI_Project/Recup_images_labellisées/yolo/dataset_complet'
#     output_folder = 'C:/Users/aerisay/Documents/AI_Project/Recup_images_labellisées/yolo/predict_images'
#     mask_reference_path = 'mask.jpg'  # Chemin vers l'image de référence pour les masques
#     # mask_output_folder = 'C:/Users/aerisay/Documents/AI_Project/Recup_images_labellisées/yolo/predict_images_mask'  # Dossier de sortie pour les masques
#     csv_output_path = 'C:/Users/aerisay/Documents/AI_Project/Recup_images_labellisées/yolo/detected_classes.csv'  # Chemin vers le fichier CSV de sortie

#     model = YOLO('yolov8m.pt')
#     model = YOLO("C:/Users/aerisay/Documents/AI_Project/Recup_images_labellisées/yolo/val/runs/detect/train4/weights/best.pt")  # load a custom model

#     # Charger l'image de référence avec OpenCV
#     reference_image = cv2.imread(mask_reference_path, cv2.IMREAD_COLOR)
#     if reference_image is None:
#         print(f"Erreur: Impossible de charger l'image de référence à partir de {mask_reference_path}. Vérifiez le chemin d'accès.")
#         return

#     # Assurez-vous que les dossiers de sortie existent
#     os.makedirs(output_folder, exist_ok=True)
#     # os.makedirs(mask_output_folder, exist_ok=True)

#     # Récupérer les chemins des images du dossier d'entrée
#     image_paths = glob.glob(os.path.join(folder_path, '*.jpg'))

#     csv_data = []

#     for image_path in image_paths:
#         # Charger l'image à traiter
#         image = cv2.imread(image_path, cv2.IMREAD_COLOR)
#         if image is None:
#             print(f"Erreur: Impossible de charger l'image à partir de {image_path}.")
#             continue

#         try:
#             # Créer le masque
#             mask = create_mask(image, reference_image)

#             # Déterminer le nom du fichier de sortie pour le masque
#             mask_filename = os.path.basename(image_path)
#             # mask_output_path = os.path.join(mask_output_folder, mask_filename)

#             # Enregistrer le masque dans le dossier de sortie
#             # cv2.imwrite(mask_output_path, mask)
#             # print(f"Masque créé et enregistré avec succès : {mask_output_path}")

#             # Effectuer la prédiction et dessiner les boîtes de délimitation
#             output_path = os.path.join(output_folder, mask_filename)
#             classes_detected = predict_and_draw_boxes(model, mask, output_path)

#             # Ajouter les résultats au CSV
#             csv_data.append({
#                 'id': mask_filename,
#                 'classes': ','.join(classes_detected),
#                 'counts': len(classes_detected)
#             })

#         except ValueError as e:
#             print(f"Erreur pour l'image {image_path}: {e}")

#     # Enregistrer les résultats dans un fichier CSV
#     df = pd.DataFrame(csv_data)
#     df.to_csv(csv_output_path, index=False)
#     print(f"Fichier CSV enregistré avec succès : {csv_output_path}")

# if __name__ == "__main__":
#     main()
