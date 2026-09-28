<template>
  <div class="box">
    <div>
      <el-input v-model="input" placeholder="请输入书名" style="width:300px"></el-input>
      <el-button type="success" @click="addBook">添加</el-button>
    </div>
    <el-table
      :data="tableData"
      style="width: 600px;">
      <el-table-column
        prop="pk"
        label="书名"
        width="180">
      </el-table-column>
      <el-table-column
        prop="fields.time"
        label="添加时间">
      </el-table-column>
    </el-table>
  </div>
</template>
 
<script>
export default {
  name: 'StudentBook',
  data () {
    return {
      input: '',
      tableData: []
    }
  },
  created () {
    this.showBook()
  },
  methods: {
    showBook () {
      this.axios.get('http://localhost:8000/show_books')
        .then((response) => {
            console.log(response.data.list);
            this.tableData = response.data.list
        })
        .catch(function (error) {
            console.log(error);
        });
    },
    addBook () {
      this.axios.get('http://localhost:8000/add_book',{params:{book_name: this.input}})
        .then((response) => {
            console.log(response.data.msg);
            this.showBook()
        })
        .catch(function (error) {
            console.log(error);
        });
    }
  }
}
</script>
 
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.box{
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}
</style>