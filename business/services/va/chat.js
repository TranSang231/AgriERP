import BaseService from "../base";
class ChatService extends BaseService {
  get entity() {
    return `va/conversations`;
  }

  loadConversations(botId){
    return this.request().get(`${this.entity}/${botId}`);
  }
  loadConversationStory(conversation_id){
    return this.request().get(`va/nlu/story?conversation_id=${conversation_id}`);
  }

  executeRasaAction(textMessage, conversationId){
    let reqMessage = {};
    reqMessage = { text: textMessage, sender: "user", conversation_id: conversationId };
    return this.request().post('/nlu/conversations/messages', JSON.stringify(reqMessage))
  }
//   getModelsByBotId(botId){
//     return this.request().get(`${this.entity}/${botId}`)
//   }
//   loadRasaModel(serverModel){
//     console.log("serverModel: ",serverModel);
    
//     return this.request().put(`/nlu/model`, { "model_file": serverModel })
//   }
//   checkRasaStatus() {
//     return "/nlu/status";
//   }
}

export default new ChatService();
