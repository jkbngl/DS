const model = tf.sequential();

// dense is "full" connected layer
const hidden = tf.layers.dense({
  units: 4, 
  inputShape: [2],
  activation: 'sigmoid'
});

// input shape is "inferred" from the previous (hidden) layer
const output = tf.layers.dense({
  units: 1,
  activation: 'sigmoid'
});

// add layers to model
model.add(hidden);
model.add(output);

// An optimizer using adam
const optimizer = tf.train.adam(0.5);

model.compile({
  optimizer: optimizer,
  loss: tf.losses.meanSquaredError
});

// training data
const xs = tf.tensor2d([
  [0, 0],
  [0, 1],
  [1, 0],
  [1, 1]
]);

// corresponding labels to the training data
const ys = tf.tensor2d([
  [0],
  [1],
  [1],
  [0]
]);



// amount of period - made global to set it to 0 when cancel training button is clicked
let period = 1000;

// output arr to display the data in the canvas
let output_arr = [];

function set_period(i)
{
  period = i;
}


// function to fill an array with data that will be used for testing
function fill_predict_tensor()
{
  let size = 10;
  let inputs = [];
  
  for (let i = 0; i < size; i++) 
  {
    for (let j = 0; j < size; j++) 
    {
       let x1 = i / size;
       let x2 = j / size; 
       
       inputs.push([x1, x2]); 
    }
  }
  
  p_xs = tf.tensor2d(inputs);

  return p_xs;
}

// display the data in the canvas
function display_data()
{
  let size = 10;
  let pos_at_arr = 0;

  // check if number should be shown
  var add_numbers = document.getElementById("check-numbers").checked;

  var c = document.getElementById("myCanvas");
  var ctx = c.getContext("2d");

  for(let j = 0; j < size; j++)
  {
    for(let k = 0; k < size; k++)
    {
      ctx.beginPath();

      
      if(!add_numbers)  // If the numbers should not be added
      {
        ctx.rect(j * 50, k * 50, 50, 50);
       
        if(output_arr[pos_at_arr] > 0.7)      // if the network is pretty certain that it is 1
          ctx.fillStyle = "black";
        else if(output_arr[pos_at_arr] > 0.4) // if the network is uncertain
          ctx.fillStyle = "gray";
        else                                  // If the network is certain that it is 0
          ctx.fillStyle = "white";

        ctx.fillText(Math.round(output_arr[pos_at_arr] * (size * 10)) / (size * 10), j * (size * 5) + 15, k * (size * 5) + 25);
        ctx.fill();
      }
      else if(add_numbers) // If the numbers should be added
      {
        ctx.fillStyle = "red"; 
        ctx.beginPath();
        ctx.fillText(Math.round(output_arr[pos_at_arr] * (size * 10)) / (size * 10), j * (size * 5) + 15, k * (size * 5) + 25);
      }

      pos_at_arr++;
    }
  }
}

train().then(() => {
  console.log('--------------- training done --------------- ');
  
  // get the tensor with the filled data 
  const ps = fill_predict_tensor();

  // make a prediction with the data from the functio
  let outputs = model.predict(ps);

  // play the tensor into an array
  output_arr = outputs.dataSync();

  console.log("Output data: ");
  console.table(output_arr);  

  // after training is done allow to change the display format
  set_buttons_active();

  display_data();

  // send a message that everything is done
  //send_message();
});

async function train() {
  

  // config for training
  const config = {
    shuffle: true,
    epochs: 10
  }

  for (let i = 0; i <= period; i++) {
    // Actual training
    const response = await model.fit(xs, ys, config);

    // Display the progress of the training
    if(i % 100 == 0 && i != 0)
      console.log( (i / 100) + " / " + (period / 100) + ": " +response.history.loss[0]);

    move((i / period)*100);
  }
}

function set_buttons_active()
{
  document.getElementById("while-training-text").innerHTML = "Select if you want to see the numbers of the output";

  // allow selections of the radio buttons
  document.getElementById("check-numbers").disabled = false;
}

function predict_inputs_ad_hoc()
{
  // Dynamically create a tensor from the input data
  const ps = tf.tensor2d([
    [document.getElementById("second-data").value, document.getElementById("first-data").value],
  ]);

  // predict by the given inputs
  let outputs = model.predict(ps);
  
  document.getElementById("predict-output").innerHTML = outputs.dataSync();
}

function move(percent_to_move) 
{
  var elem = document.getElementById("myBar");   
  elem.style.width = percent_to_move + '%'; 
  elem.innerHTML = "&nbsp;" + percent_to_move.toFixed(2) + "%"; 
  // elem.innerHTML = percent_to_move * 1 + '%';
}

function send_message()
{
  // https://api.telegram.org/bot802113499:AAF09QJDBSpkwzajMEdowPmr7f_yc5S6TbE/getUpdates
  const TelegramBot = require('node-telegram-bot-api');

  // replace the value below with the Telegram token you receive from @BotFather
  const token = '802113499:AAF09QJDBSpkwzajMEdowPmr7f_yc5S6TbE';

  // Create a bot that uses 'polling' to fetch new updates
  const bot = new TelegramBot(token, {polling: true});

  bot.sendMessage('-353232539', 'Received your message');
}