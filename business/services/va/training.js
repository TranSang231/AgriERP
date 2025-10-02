import BaseService from "../base";

class TrainingService extends BaseService {
  get entity() {
    return `va/nlu`;
  }

  trainingUsingRawData(botToTrain, comment, rawData) {
    console.log(
      "botToTrain: ",
      botToTrain,
      "comment: ",
      comment,
      "rawData: ",
      rawData
    );

    return this.request().post(
      `${this.entity}/model/train?bot_name=${botToTrain.bot_name}&bot_id=${botToTrain.id}&comment=${comment}`,
      rawData
    );
  }

  async trainingUsingRawDataFile(botToTrain, comment, rawData) {
    console.log("botToTrain:", botToTrain, "comment:", comment);

    const blob = new Blob([rawData], { type: "application/x-yaml" });
    const formData = new FormData();
    formData.append("file", blob, "data.yml");
    formData.append("comment", comment);

    return this.request().post(
      `${this.entity}/model/train?bot_name=${botToTrain.bot_name}&bot_id=${botToTrain.id}`,
      formData,
      // {
      //   headers: { "Content-Type": "multipart/form-data" },
      // }
    );
  }
}

export default new TrainingService();
