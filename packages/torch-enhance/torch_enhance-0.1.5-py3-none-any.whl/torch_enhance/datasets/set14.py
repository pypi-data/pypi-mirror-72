import os
from dataclasses import dataclass

import torchvision.transforms as T

from .base import SET14_URL, BaseDataset


@dataclass()
class Set14(BaseDataset):

    scale_factor: int = 2
    image_size: int = 256
    color_space: str = "RGB"
    data_dir: str = ""
    lr_transforms: T.Compose = None
    hr_transforms: T.Compose = None

    def __post_init__(self):

        self.url = SET14_URL
        self.extensions = [".png"]

        if self.data_dir == "":
            self.data_dir = os.path.join(os.getcwd(), self.base_dir)

        self.root_dir = os.path.join(self.data_dir, "Set14")
        self.download_google_drive(self.data_dir, filename="Set14.zip")
        self.file_names = self.get_files(self.root_dir)

        if self.lr_transforms is None:
            self.lr_transform = self.get_lr_transforms()
        if self.hr_transforms is None:
            self.hr_transform = self.get_hr_transforms()
